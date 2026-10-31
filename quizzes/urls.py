from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('config/', views.quiz_config_view, name='config'),
    path('start/', views.quiz_start_view, name='start'),
    path('take/<int:attempt_id>/', views.quiz_take_view, name='take'),
    path('save-answer/<int:attempt_id>/', views.quiz_save_answer_api, name='save_answer'),
    path('submit/<int:attempt_id>/', views.quiz_submit_view, name='submit'),
    path('result/<int:attempt_id>/', views.quiz_result_view, name='result'),
    path('history/', views.quiz_history_view, name='history'),
]
