from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from questions.models import Category, Topic, Question
from quizzes.models import QuizAttempt
from .services import get_user_dashboard_analytics

def landing_page_view(request):
    """
    Landing page showcasing the learning platform, features, and paths.
    """
    total_questions = Question.objects.filter(is_active=True).count()
    python_count = Question.objects.filter(is_active=True, topic__category__technology='PYTHON').count()
    django_count = Question.objects.filter(is_active=True, topic__category__technology='DJANGO').count()
    categories_count = Category.objects.count()
    topics_count = Topic.objects.count()

    categories = Category.objects.prefetch_related('topics').all()

    context = {
        'total_questions': total_questions,
        'python_count': python_count,
        'django_count': django_count,
        'categories_count': categories_count,
        'topics_count': topics_count,
        'categories': categories,
    }
    return render(request, 'dashboard/landing.html', context)

@login_required
def dashboard_view(request):
    """
    Authenticated developer dashboard with live statistics, charts, and recommendations.
    """
    analytics = get_user_dashboard_analytics(request.user)
    return render(request, 'dashboard/dashboard.html', {
        'analytics': analytics,
        'user': request.user,
    })

@login_required
def learning_progress_view(request):
    """
    Granular syllabus view showing progress across every Category and Topic.
    """
    analytics = get_user_dashboard_analytics(request.user)
    topic_map = {t['id']: t for t in analytics['all_topic_stats']}

    categories = Category.objects.prefetch_related('topics').all()
    categories_with_progress = []

    for cat in categories:
        cat_topics = []
        cat_total_questions = 0
        cat_attempted = 0
        cat_correct = 0

        for t in cat.topics.all():
            q_count = t.questions.filter(is_active=True).count()
            cat_total_questions += q_count
            stat = topic_map.get(t.id, {'total': 0, 'correct': 0, 'accuracy': 0})
            cat_attempted += stat['total']
            cat_correct += stat['correct']

            cat_topics.append({
                'topic': t,
                'question_count': q_count,
                'attempted': stat['total'],
                'correct': stat['correct'],
                'accuracy': stat['accuracy'],
            })

        cat_accuracy = round((cat_correct / cat_attempted * 100)) if cat_attempted > 0 else 0
        categories_with_progress.append({
            'category': cat,
            'topics': cat_topics,
            'total_questions': cat_total_questions,
            'attempted': cat_attempted,
            'correct': cat_correct,
            'accuracy': cat_accuracy,
        })

    return render(request, 'dashboard/progress.html', {
        'categories_with_progress': categories_with_progress,
        'analytics': analytics,
    })
