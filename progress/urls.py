from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('syllabus/', views.learning_progress_view, name='syllabus'),
]
