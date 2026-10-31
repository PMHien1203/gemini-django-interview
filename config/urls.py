"""
URL configuration for Python & Django Interview Master.
"""
from django.contrib import admin
from django.urls import path, include
from progress.views import landing_page_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page_view, name='home'),
    path('auth/', include('accounts.urls', namespace='accounts')),
    path('questions/', include('questions.urls', namespace='questions')),
    path('quiz/', include('quizzes.urls', namespace='quizzes')),
    path('dashboard/', include('progress.urls', namespace='progress')),
]
