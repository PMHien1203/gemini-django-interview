from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Topic, Question, AnswerOption

def question_list_view(request):
    """
    Searchable, filterable question bank view.
    """
    qs = Question.objects.filter(is_active=True).select_related('topic', 'topic__category').prefetch_related('options')

    tech = request.GET.get('technology', '').strip()
    topic_id = request.GET.get('topic', '').strip()
    difficulty = request.GET.get('difficulty', '').strip()
    search = request.GET.get('q', '').strip()

    if tech in ['PYTHON', 'DJANGO']:
        qs = qs.filter(topic__category__technology=tech)

    if topic_id and topic_id.isdigit():
        qs = qs.filter(topic_id=int(topic_id))

    if difficulty in ['BEGINNER', 'INTERMEDIATE', 'ADVANCED']:
        qs = qs.filter(difficulty=difficulty)

    if search:
        qs = qs.filter(
            Q(content__icontains=search) |
            Q(explanation__icontains=search) |
            Q(code_snippet__icontains=search) |
            Q(topic__name__icontains=search)
        )

    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.prefetch_related('topics').all()
    topics = Topic.objects.select_related('category').all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'topics': topics,
        'selected_tech': tech,
        'selected_topic': int(topic_id) if topic_id.isdigit() else None,
        'selected_difficulty': difficulty,
        'search_query': search,
        'total_count': qs.count(),
    }
    return render(request, 'questions/question_list.html', context)

def question_detail_view(request, question_id):
    """
    In-depth study card for an interview question.
    """
    question = get_object_or_404(
        Question.objects.select_related('topic', 'topic__category').prefetch_related('options'),
        id=question_id,
        is_active=True
    )
    related_questions = Question.objects.filter(
        topic=question.topic,
        is_active=True
    ).exclude(id=question.id)[:4]

    return render(request, 'questions/question_detail.html', {
        'question': question,
        'related_questions': related_questions,
    })
