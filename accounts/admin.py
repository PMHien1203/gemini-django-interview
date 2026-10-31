from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_role', 'experience_level', 'streak_count', 'last_active_date', 'preferred_theme')
    search_fields = ('user__username', 'user__email', 'target_role')
    list_filter = ('target_role', 'experience_level', 'preferred_theme')
