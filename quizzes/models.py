from django.db import models
from django.contrib.auth.models import User
from questions.models import Question, AnswerOption, Topic
from django.utils import timezone

class Quiz(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('PRACTICE', 'Practice Mode (Instant Feedback)'),
        ('EXAM', 'Exam Mode (Timed, Graded)'),
        ('TOPIC_PRACTICE', 'Topic Drill'),
        ('MOCK_INTERVIEW', 'Full Mock Interview'),
    ]
    DIFFICULTY_CHOICES = [
        ('ALL', 'Mixed Difficulties'),
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    quiz_type = models.CharField(max_length=30, choices=QUIZ_TYPE_CHOICES, default='EXAM')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='ALL')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='quizzes')
    total_questions = models.PositiveIntegerField(default=20)
    time_limit = models.PositiveIntegerField(default=1200, help_text="Time limit in seconds (e.g. 1200 for 20 minutes)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Quizzes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_quiz_type_display()})"

class QuizAttempt(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ABANDONED', 'Abandoned'),
    ]
    MODE_CHOICES = [
        ('PRACTICE', 'Practice'),
        ('EXAM', 'Exam'),
        ('TOPIC_PRACTICE', 'Topic Practice'),
        ('MOCK_INTERVIEW', 'Mock Interview'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True, related_name='attempts')
    title = models.CharField(max_length=255)
    mode = models.CharField(max_length=30, choices=MODE_CHOICES, default='EXAM')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(default=0.0) # percentage
    correct_count = models.IntegerField(default=0)
    incorrect_count = models.IntegerField(default=0)
    unanswered_count = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    time_spent = models.IntegerField(default=0) # elapsed seconds
    time_limit = models.IntegerField(default=1200) # seconds allowed
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS', db_index=True)

    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', '-completed_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.status}) - {self.score}%"

    @property
    def is_passed(self):
        return self.score >= 70.0

    @property
    def formatted_time_spent(self):
        mins = self.time_spent // 60
        secs = self.time_spent % 60
        return f"{mins}m {secs}s"

class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    selected_option = models.ForeignKey(AnswerOption, on_delete=models.SET_NULL, null=True, blank=True, related_name='selected_by')
    is_correct = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    order_index = models.PositiveIntegerField(default=0)
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order_index', 'id']
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"Attempt #{self.attempt_id} - Q#{self.question_id}: {'Correct' if self.is_correct else 'Incorrect'}"
