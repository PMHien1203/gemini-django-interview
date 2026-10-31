from django.db.models import Avg, Max, Count, Sum
from quizzes.models import QuizAttempt, UserAnswer
from questions.models import Question, Topic, Category

def get_user_dashboard_analytics(user):
    """
    Computes aggregated performance metrics and Chart.js datasets for the user dashboard.
    """
    completed_attempts = QuizAttempt.objects.filter(
        user=user, status='COMPLETED'
    ).order_by('-completed_at')

    total_tests = completed_attempts.count()

    if total_tests == 0:
        avg_score = 0.0
        highest_score = 0.0
    else:
        avg_score = round(completed_attempts.aggregate(Avg('score'))['score__avg'] or 0.0, 1)
        highest_score = round(completed_attempts.aggregate(Max('score'))['score__max'] or 0.0, 1)

    # All answered user questions
    user_answers = UserAnswer.objects.filter(
        attempt__user=user,
        attempt__status='COMPLETED',
        selected_option__isnull=False
    ).select_related('question__topic__category', 'question__topic')

    total_questions_completed = user_answers.count()

    # Python vs Django breakdown
    python_answers = [ua for ua in user_answers if ua.question.topic.category.technology == 'PYTHON']
    django_answers = [ua for ua in user_answers if ua.question.topic.category.technology == 'DJANGO']

    py_total = len(python_answers)
    py_correct = sum(1 for ua in python_answers if ua.is_correct)
    py_progress = round((py_correct / py_total * 100), 1) if py_total > 0 else 0.0

    dj_total = len(django_answers)
    dj_correct = sum(1 for ua in django_answers if ua.is_correct)
    dj_progress = round((dj_correct / dj_total * 100), 1) if dj_total > 0 else 0.0

    # Topic-level performance
    topic_map = {}
    for ua in user_answers:
        t = ua.question.topic
        if t.id not in topic_map:
            topic_map[t.id] = {
                'id': t.id,
                'name': t.name,
                'technology': t.category.technology,
                'total': 0,
                'correct': 0,
            }
        topic_map[t.id]['total'] += 1
        if ua.is_correct:
            topic_map[t.id]['correct'] += 1

    topic_stats = []
    for t_id, data in topic_map.items():
        pct = round((data['correct'] / data['total']) * 100) if data['total'] > 0 else 0
        topic_stats.append({
            'id': data['id'],
            'name': data['name'],
            'technology': data['technology'],
            'total': data['total'],
            'correct': data['correct'],
            'accuracy': pct,
        })

    # Sort to find weakest and strongest
    weakest_topics = sorted([t for t in topic_stats if t['total'] >= 1], key=lambda x: (x['accuracy'], -x['total']))[:4]
    strongest_topics = sorted([t for t in topic_stats if t['total'] >= 1], key=lambda x: (-x['accuracy'], -x['total']))[:4]

    # Recommended topics: either weakest, or if none, high-yield topics
    recommended_topics = []
    if weakest_topics:
        recommended_topics = weakest_topics
    else:
        # Default recommendations from database
        sample_topics = Topic.objects.select_related('category')[:4]
        for st in sample_topics:
            recommended_topics.append({
                'id': st.id,
                'name': st.name,
                'technology': st.category.technology,
                'total': 0,
                'correct': 0,
                'accuracy': 0,
            })

    # Recent attempts (last 5)
    recent_attempts = completed_attempts[:5]

    # Chart.js data: Score History (up to last 10 attempts chronologically)
    history_attempts = list(reversed(completed_attempts[:10]))
    chart_score_labels = [f"Quiz #{a.id} ({a.mode[:4]})" for a in history_attempts]
    chart_scores = [round(a.score, 1) for a in history_attempts]

    # Chart.js data: Topic Accuracy (Top 6 most practiced topics)
    top_topics = sorted(topic_stats, key=lambda x: x['total'], reverse=True)[:6]
    chart_topic_labels = [t['name'] for t in top_topics]
    chart_topic_accuracies = [t['accuracy'] for t in top_topics]

    streak = getattr(user.profile, 'streak_count', 1) if hasattr(user, 'profile') else 1

    return {
        'total_questions_completed': total_questions_completed,
        'total_tests': total_tests,
        'avg_score': avg_score,
        'highest_score': highest_score,
        'streak': streak,
        'py_progress': py_progress,
        'py_total': py_total,
        'py_correct': py_correct,
        'dj_progress': dj_progress,
        'dj_total': dj_total,
        'dj_correct': dj_correct,
        'weakest_topics': weakest_topics,
        'strongest_topics': strongest_topics,
        'recommended_topics': recommended_topics,
        'recent_attempts': recent_attempts,
        'chart_score_labels': chart_score_labels,
        'chart_scores': chart_scores,
        'chart_topic_labels': chart_topic_labels,
        'chart_topic_accuracies': chart_topic_accuracies,
        'all_topic_stats': topic_stats,
    }
