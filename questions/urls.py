from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.question_list_view, name='list'),
    path('<int:question_id>/', views.question_detail_view, name='detail'),
]
