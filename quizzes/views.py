import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from questions.models import Category, Topic, Question, AnswerOption
from .models import Quiz, QuizAttempt, UserAnswer
from .services import (
    generate_quiz_attempt,
    save_single_answer,
    submit_quiz_attempt,
    get_detailed_attempt_report,
)

@login_required
def quiz_config_view(request):
    """
    Configure custom quiz, practice drill, or full mock interview.
    """
    categories = Category.objects.prefetch_related('topics').all()
    topics = Topic.objects.select_related('category').all()

    # Pre-selected values from query params
    initial_mode = request.GET.get('mode', 'EXAM')
    initial_tech = request.GET.get('tech', '')
    initial_topic_id = request.GET.get('topic_id', '')
    initial_difficulty = request.GET.get('difficulty', 'ALL')

    context = {
        'categories': categories,
        'topics': topics,
        'initial_mode': initial_mode,
        'initial_tech': initial_tech,
        'initial_topic_id': initial_topic_id,
        'initial_difficulty': initial_difficulty,
    }
    return render(request, 'quizzes/quiz_config.html', context)

@login_required
@require_POST
def quiz_start_view(request):
    """
    Creates an attempt from configuration POST data and redirects to quiz interface.
    """
    mode = request.POST.get('mode', 'EXAM')
    technology = request.POST.get('technology', '').strip() or None
    topic_id = request.POST.get('topic_id', '').strip()
    topic_id = int(topic_id) if topic_id and topic_id.isdigit() else None
    difficulty = request.POST.get('difficulty', 'ALL')
    question_count = int(request.POST.get('question_count', 15))
    time_limit_mins = int(request.POST.get('time_limit_mins', 15))
    time_limit_sec = time_limit_mins * 60 if time_limit_mins > 0 else 0

    try:
        attempt = generate_quiz_attempt(
            user=request.user,
            mode=mode,
            technology=technology,
            topic_id=topic_id,
            difficulty=difficulty,
            question_count=question_count,
            time_limit=time_limit_sec,
        )
        return redirect('quizzes:take', attempt_id=attempt.id)
    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('quizzes:config')

@login_required
def quiz_take_view(request, attempt_id):
    """
    Single-question-per-screen quiz engine with real-time state, countdown timer,
    palette navigation, review flagging, and instant practice mode feedback.
    """
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    if attempt.user != request.user:
        raise PermissionDenied("You do not have permission to access this quiz session.")

    if attempt.status == 'COMPLETED':
        messages.info(request, "This quiz has already been submitted.")
        return redirect('quizzes:result', attempt_id=attempt.id)

    # Fetch all user answers ordered
    user_answers = list(
        UserAnswer.objects.filter(attempt=attempt)
        .select_related('question', 'question__topic', 'question__topic__category', 'selected_option')
        .prefetch_related('question__options')
        .order_by('order_index')
    )

    if not user_answers:
        messages.error(request, "No questions found in this quiz attempt.")
        return redirect('quizzes:config')

    total_questions = len(user_answers)
    current_idx_str = request.GET.get('q', '1')
    try:
        current_idx = int(current_idx_str)
        if current_idx < 1 or current_idx > total_questions:
            current_idx = 1
    except ValueError:
        current_idx = 1

    current_ua = user_answers[current_idx - 1]
    current_question = current_ua.question

    # Prepare questions data for JavaScript client navigation
    palette_data = []
    for idx, ua in enumerate(user_answers, start=1):
        palette_data.append({
            'index': idx,
            'question_id': ua.question_id,
            'is_answered': ua.selected_option_id is not None,
            'is_flagged': ua.is_flagged,
            'is_current': (idx == current_idx),
        })

    # Prepare all options for current question with deterministic shuffle
    options = list(current_question.options.all())
    # Randomize deterministically based on attempt id + question id
    random_seed = attempt.id * 1000 + current_question.id
    import random
    rng = random.Random(random_seed)
    rng.shuffle(options)

    # If practice mode, we can show explanation if answered
    show_explanation = (attempt.mode == 'PRACTICE' and current_ua.selected_option_id is not None)

    context = {
        'attempt': attempt,
        'current_index': current_idx,
        'total_questions': total_questions,
        'current_ua': current_ua,
        'current_question': current_question,
        'options': options,
        'palette_data': palette_data,
        'show_explanation': show_explanation,
        'has_prev': current_idx > 1,
        'has_next': current_idx < total_questions,
        'prev_idx': current_idx - 1,
        'next_idx': current_idx + 1,
        'time_limit_sec': attempt.time_limit,
    }
    return render(request, 'quizzes/quiz_take.html', context)

@login_required
@require_POST
def quiz_save_answer_api(request, attempt_id):
    """
    AJAX endpoint for instantaneous answer persistence & flag toggles without page reload.
    """
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    if attempt.user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    if attempt.status == 'COMPLETED':
        return JsonResponse({'error': 'Quiz already completed'}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    question_id = data.get('question_id')
    option_id = data.get('option_id')
    is_flagged = data.get('is_flagged')

    if not question_id:
        return JsonResponse({'error': 'Missing question_id'}, status=400)

    ua = save_single_answer(
        attempt=attempt,
        user=request.user,
        question_id=question_id,
        option_id=option_id,
        is_flagged=is_flagged,
    )

    if not ua:
        return JsonResponse({'error': 'Could not update answer'}, status=400)

    response_data = {
        'success': True,
        'is_answered': ua.selected_option_id is not None,
        'is_flagged': ua.is_flagged,
    }

    # In practice mode, return the explanation and whether chosen is correct
    if attempt.mode == 'PRACTICE' and ua.selected_option:
        correct_option = ua.question.options.filter(is_correct=True).first()
        response_data['is_correct'] = ua.is_correct
        response_data['explanation'] = ua.question.explanation
        response_data['correct_option_id'] = correct_option.id if correct_option else None
        response_data['selected_explanation'] = ua.selected_option.explanation

    return JsonResponse(response_data)

@login_required
@require_POST
def quiz_submit_view(request, attempt_id):
    """
    Finalizes attempt, runs server-side grading inside atomic transaction,
    redirects to results.
    """
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    if attempt.user != request.user:
        raise PermissionDenied("Unauthorized quiz submission.")

    elapsed_time = request.POST.get('time_spent', 0)
    try:
        elapsed_sec = int(elapsed_time)
    except ValueError:
        elapsed_sec = 0

    # Collect any answers passed via form payload
    raw_answers = {}
    for key, val in request.POST.items():
        if key.startswith('q_'):
            qid = key.split('_')[1]
            raw_answers[qid] = val

    updated_attempt = submit_quiz_attempt(
        attempt_id=attempt.id,
        user=request.user,
        raw_answers_dict=raw_answers,
        elapsed_time_sec=elapsed_sec,
    )

    messages.success(request, f"Quiz submitted! Your score: {updated_attempt.score}%")
    return redirect('quizzes:result', attempt_id=updated_attempt.id)

@login_required
def quiz_result_view(request, attempt_id):
    """
    Detailed results dashboard showing score, pass/fail status, performance by topic,
    and granular review of every question with explanation and rationale.
    """
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    if attempt.user != request.user:
        raise PermissionDenied("You do not have permission to view this result.")

    report = get_detailed_attempt_report(attempt)

    return render(request, 'quizzes/quiz_result.html', {
        'attempt': attempt,
        'report': report,
        'topic_breakdown': report['topic_breakdown'],
        'detailed_questions': report['detailed_questions'],
    })

@login_required
def quiz_history_view(request):
    """
    Complete history of all attempts taken by the current user.
    """
    attempts_qs = QuizAttempt.objects.filter(user=request.user).order_by('-started_at')
    paginator = Paginator(attempts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'quizzes/quiz_history.html', {
        'page_obj': page_obj,
    })
