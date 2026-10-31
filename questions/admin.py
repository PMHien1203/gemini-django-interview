from django.contrib import admin
from .models import Category, Topic, Question, AnswerOption

class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 4
    min_num = 2
    fields = ('content', 'is_correct', 'explanation')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'technology', 'slug')
    list_filter = ('technology',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category__technology', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'topic', 'difficulty', 'is_active', 'created_at')
    list_filter = ('difficulty', 'is_active', 'topic__category__technology', 'topic__category', 'topic')
    search_fields = ('content', 'explanation', 'code_snippet')
    inlines = [AnswerOptionInline]
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected questions as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected questions as inactive"

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('content', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('content', 'explanation')
