from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

class Category(models.Model):
    TECH_CHOICES = [
        ('PYTHON', 'Python'),
        ('DJANGO', 'Django'),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    technology = models.CharField(max_length=20, choices=TECH_CHOICES)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['technology', 'name']

    def __str__(self):
        return f"{self.get_technology_display()} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.technology}-{self.name}")
        super().save(*args, **kwargs)

class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('category', 'slug')
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.category.name} > {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]
    QUESTION_TYPE_CHOICES = [
        ('SINGLE_CHOICE', 'Single Choice'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField(help_text="The interview question text.")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, db_index=True)
    explanation = models.TextField(help_text="Detailed technical rationale and why other options are incorrect.")
    code_snippet = models.TextField(blank=True, default='', help_text="Optional Python or Django code block.")
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPE_CHOICES, default='SINGLE_CHOICE')
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['difficulty', 'is_active']),
            models.Index(fields=['topic', 'difficulty']),
        ]

    def __str__(self):
        snippet = (self.content[:60] + '...') if len(self.content) > 60 else self.content
        return f"[{self.difficulty}] {snippet}"

    @property
    def correct_option(self):
        return self.options.filter(is_correct=True).first()

    def clean(self):
        if self.pk:
            options_count = self.options.count()
            if options_count > 0:
                correct_count = self.options.filter(is_correct=True).count()
                if correct_count != 1:
                    raise ValidationError("Single-choice questions must have exactly one correct answer option.")
                if options_count < 2:
                    raise ValidationError("Question must have at least two answer options.")

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    content = models.TextField()
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True, default='', help_text="Why this option is correct or incorrect.")

    class Meta:
        ordering = ['id']

    def __str__(self):
        prefix = "[✓]" if self.is_correct else "[ ]"
        snippet = (self.content[:50] + '...') if len(self.content) > 50 else self.content
        return f"{prefix} {snippet}"
