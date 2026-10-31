from django.contrib import admin
from .models import Quiz, QuizAttempt, UserAnswer

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ('question', 'selected_option', 'is_correct', 'is_flagged', 'order_index', 'answered_at')
    can_delete = False

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'quiz_type', 'difficulty', 'total_questions', 'time_limit', 'is_active', 'created_at')
    list_filter = ('quiz_type', 'difficulty', 'is_active')
    search_fields = ('title',)

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'mode', 'score', 'status', 'started_at', 'completed_at', 'time_spent')
    list_filter = ('mode', 'status', 'started_at')
    search_fields = ('user__username', 'title')
    inlines = [UserAnswerInline]

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct', 'is_flagged')
    list_filter = ('is_correct', 'is_flagged')
