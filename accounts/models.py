from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('junior', 'Junior Python Developer'),
        ('mid', 'Mid-Level Python & Django Developer'),
        ('senior', 'Senior Python / Backend Architect'),
        ('fullstack', 'Django Full-Stack Engineer'),
    ]
    LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    target_role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='mid')
    experience_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='INTERMEDIATE')
    bio = models.TextField(blank=True, default='')
    streak_count = models.PositiveIntegerField(default=1)
    last_active_date = models.DateField(default=timezone.localdate)
    preferred_theme = models.CharField(max_length=10, default='dark', choices=[('dark', 'Dark'), ('light', 'Light')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def update_streak(self):
        today = timezone.localdate()
        last_date = self.last_active_date
        if hasattr(last_date, 'date'):
            last_date = last_date.date()
        if not last_date:
            last_date = today

        if last_date == today:
            return
        elif last_date == today - timezone.timedelta(days=1):
            self.streak_count += 1
        elif last_date < today - timezone.timedelta(days=1):
            self.streak_count = 1
        self.last_active_date = today
        self.save(update_fields=['streak_count', 'last_active_date'])
