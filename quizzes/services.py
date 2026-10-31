import random
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import PermissionDenied, ValidationError
from questions.models import Question, AnswerOption, Topic
from .models import QuizAttempt, UserAnswer

def generate_quiz_attempt(user, mode='EXAM', technology=None, topic_id=None, difficulty='ALL', question_count=20, time_limit=1200, title=None):
    """
    Assembles questions matching criteria and seeds a unique QuizAttempt with randomized options.
    """
    qs = Question.objects.filter(is_active=True).select_related('topic', 'topic__category')

    if technology in ['PYTHON', 'DJANGO']:
        qs = qs.filter(topic__category__technology=technology)

    if topic_id:
        qs = qs.filter(topic_id=topic_id)

    if difficulty in ['BEGINNER', 'INTERMEDIATE', 'ADVANCED']:
        qs = qs.filter(difficulty=difficulty)

    available_pks = list(qs.values_list('id', flat=True))
    if not available_pks:
        raise ValidationError("No active questions found matching the selected criteria.")

    selected_count = min(int(question_count), len(available_pks))
    chosen_pks = random.sample(available_pks, selected_count)

    if not title:
        if mode == 'MOCK_INTERVIEW':
            title = f"Full Mock Technical Interview ({selected_count} Questions)"
        elif topic_id:
            topic = Topic.objects.get(id=topic_id)
            title = f"Topic Drill: {topic.name} ({difficulty})"
        elif technology:
            title = f"{technology.title()} Mastery Exam ({difficulty})"
        else:
            title = f"Python & Django Knowledge Check ({difficulty})"

    # In practice mode, time limit can be set to 0 (unlimited)
    if mode == 'PRACTICE' and (time_limit is None or time_limit <= 0):
        actual_time_limit = 0
    else:
        actual_time_limit = time_limit or 1200

    with transaction.atomic():
        attempt = QuizAttempt.objects.create(
            user=user,
            title=title,
            mode=mode,
            time_limit=actual_time_limit,
            total_questions=selected_count,
            status='IN_PROGRESS',
        )

        user_answers = [
            UserAnswer(
                attempt=attempt,
                question_id=qid,
                order_index=idx + 1,
            )
            for idx, qid in enumerate(chosen_pks)
        ]
        UserAnswer.objects.bulk_create(user_answers)

    return attempt

def save_single_answer(attempt, user, question_id, option_id=None, is_flagged=None):
    """
    Saves an intermediate answer or review flag during the quiz session.
    Guarantees user isolation.
    """
    if attempt.user != user:
        raise PermissionDenied("You are not authorized to update this attempt.")
    if attempt.status != 'IN_PROGRESS':
        return None

    try:
        user_answer = UserAnswer.objects.get(attempt=attempt, question_id=question_id)
    except UserAnswer.DoesNotExist:
        return None

    if option_id is not None:
        if option_id == 0 or option_id == '':
            user_answer.selected_option = None
            user_answer.is_correct = False
        else:
            try:
                option = AnswerOption.objects.get(id=option_id, question_id=question_id)
                user_answer.selected_option = option
                user_answer.is_correct = option.is_correct
            except AnswerOption.DoesNotExist:
                user_answer.selected_option = None
                user_answer.is_correct = False

    if is_flagged is not None:
        user_answer.is_flagged = bool(is_flagged)

    user_answer.save()
    return user_answer

def submit_quiz_attempt(attempt_id, user, raw_answers_dict=None, elapsed_time_sec=0):
    """
    Submits a quiz attempt, computes scores purely server-side with atomic transaction.
    Guarantees idempotence: if already completed, returns existing attempt.
    """
    with transaction.atomic():
        attempt = QuizAttempt.objects.select_for_update().get(id=attempt_id)
        if attempt.user != user:
            raise PermissionDenied("Unauthorized quiz submission.")

        if attempt.status == 'COMPLETED':
            return attempt

        user_answers = list(UserAnswer.objects.filter(attempt=attempt).select_related('question'))

        if raw_answers_dict:
            for ua in user_answers:
                qid_str = str(ua.question_id)
                if qid_str in raw_answers_dict:
                    opt_id_val = raw_answers_dict[qid_str]
                    if opt_id_val:
                        try:
                            option = AnswerOption.objects.get(id=int(opt_id_val), question=ua.question)
                            ua.selected_option = option
                            ua.is_correct = option.is_correct
                        except (AnswerOption.DoesNotExist, ValueError):
                            ua.selected_option = None
                            ua.is_correct = False
                    ua.save()

        # Calculate backend score
        total_questions = len(user_answers)
        correct_count = sum(1 for ua in user_answers if ua.selected_option and ua.is_correct)
        unanswered_count = sum(1 for ua in user_answers if not ua.selected_option)
        incorrect_count = total_questions - correct_count - unanswered_count

        score_pct = round((correct_count / total_questions * 100.0), 1) if total_questions > 0 else 0.0

        attempt.score = score_pct
        attempt.correct_count = correct_count
        attempt.incorrect_count = incorrect_count
        attempt.unanswered_count = unanswered_count
        attempt.total_questions = total_questions
        attempt.time_spent = min(int(elapsed_time_sec), attempt.time_limit if attempt.time_limit > 0 else 999999)
        attempt.status = 'COMPLETED'
        attempt.completed_at = timezone.now()
        attempt.save()

    return attempt

def get_detailed_attempt_report(attempt):
    """
    Compiles detailed breakdown for the results page, including topic statistics.
    """
    user_answers = UserAnswer.objects.filter(attempt=attempt).select_related(
        'question', 'question__topic', 'question__topic__category', 'selected_option'
    ).prefetch_related('question__options')

    topic_stats = {}
    detailed_questions = []

    for ua in user_answers:
        q = ua.question
        topic_name = q.topic.name
        tech = q.topic.category.technology

        if topic_name not in topic_stats:
            topic_stats[topic_name] = {'total': 0, 'correct': 0, 'technology': tech}
        topic_stats[topic_name]['total'] += 1
        if ua.is_correct:
            topic_stats[topic_name]['correct'] += 1

        correct_opt = next((opt for opt in q.options.all() if opt.is_correct), None)

        detailed_questions.append({
            'user_answer': ua,
            'question': q,
            'selected_option': ua.selected_option,
            'correct_option': correct_opt,
            'is_correct': ua.is_correct,
            'is_unanswered': ua.selected_option is None,
            'is_flagged': ua.is_flagged,
            'options': list(q.options.all()),
        })

    topic_breakdown = []
    for name, data in topic_stats.items():
        pct = round((data['correct'] / data['total']) * 100) if data['total'] > 0 else 0
        topic_breakdown.append({
            'topic': name,
            'technology': data['technology'],
            'total': data['total'],
            'correct': data['correct'],
            'percentage': pct,
            'mastered': pct >= 70,
        })

    return {
        'attempt': attempt,
        'detailed_questions': detailed_questions,
        'topic_breakdown': topic_breakdown,
    }
