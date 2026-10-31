from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from django.utils import timezone
from questions.models import Category, Topic, Question, AnswerOption
from quizzes.models import QuizAttempt, UserAnswer

from questions.fixtures_data.python_beginner import PYTHON_BEGINNER_QUESTIONS
from questions.fixtures_data.python_intermediate import PYTHON_INTERMEDIATE_QUESTIONS
from questions.fixtures_data.python_advanced import PYTHON_ADVANCED_QUESTIONS
from questions.fixtures_data.django_beginner import DJANGO_BEGINNER_QUESTIONS
from questions.fixtures_data.django_intermediate import DJANGO_INTERMEDIATE_QUESTIONS
from questions.fixtures_data.django_advanced import DJANGO_ADVANCED_QUESTIONS

class Command(BaseCommand):
    help = 'Seeds initial 240+ comprehensive Python & Django interview questions idempotently.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding for Python & Django Interview Master..."))

        all_datasets = [
            ("PYTHON", PYTHON_BEGINNER_QUESTIONS),
            ("PYTHON", PYTHON_INTERMEDIATE_QUESTIONS),
            ("PYTHON", PYTHON_ADVANCED_QUESTIONS),
            ("DJANGO", DJANGO_BEGINNER_QUESTIONS),
            ("DJANGO", DJANGO_INTERMEDIATE_QUESTIONS),
            ("DJANGO", DJANGO_ADVANCED_QUESTIONS),
        ]

        total_seeded = 0
        total_options = 0

        with transaction.atomic():
            for tech, dataset in all_datasets:
                for item in dataset:
                    cat_name = item['category']
                    cat_tech = tech
                    cat_slug = f"{cat_tech.lower()}-{cat_name.lower().replace(' ', '-')}"

                    category, _ = Category.objects.get_or_create(
                        slug=cat_slug,
                        defaults={
                            'name': cat_name,
                            'technology': cat_tech,
                            'description': f"Core interview concepts for {cat_name}.",
                        }
                    )

                    topic_name = item['topic']
                    topic_slug = topic_name.lower().replace(' ', '-').replace('*', '').replace('(', '').replace(')', '').replace('/', '-')
                    topic, _ = Topic.objects.get_or_create(
                        category=category,
                        slug=topic_slug,
                        defaults={
                            'name': topic_name,
                            'description': f"Technical depth on {topic_name}.",
                        }
                    )

                    # Question idempotency by content
                    question, created = Question.objects.get_or_create(
                        content=item['content'],
                        defaults={
                            'topic': topic,
                            'difficulty': item['difficulty'],
                            'explanation': item['explanation'],
                            'code_snippet': item.get('code_snippet', ''),
                            'question_type': 'SINGLE_CHOICE',
                            'is_active': True,
                        }
                    )

                    if created:
                        total_seeded += 1
                        for opt_text, is_correct, opt_exp in item['options']:
                            AnswerOption.objects.create(
                                question=question,
                                content=opt_text,
                                is_correct=is_correct,
                                explanation=opt_exp,
                            )
                            total_options += 1
                    else:
                        # Ensure options exist
                        if question.options.count() == 0:
                            for opt_text, is_correct, opt_exp in item['options']:
                                AnswerOption.objects.create(
                                    question=question,
                                    content=opt_text,
                                    is_correct=is_correct,
                                    explanation=opt_exp,
                                )
                                total_options += 1

            # Seed demo user & initial attempt history for rich dashboard
            demo_user, u_created = User.objects.get_or_create(
                username='demo_developer',
                defaults={
                    'email': 'developer@interviewmaster.io',
                    'first_name': 'Alex',
                    'last_name': 'Rivera',
                }
            )
            if u_created:
                demo_user.set_password('DjangoPython2026!')
                demo_user.save()
                demo_user.profile.target_role = 'senior'
                demo_user.profile.experience_level = 'ADVANCED'
                demo_user.profile.bio = 'Senior Python & Django Backend Engineer preparing for staff interview loops.'
                demo_user.profile.streak_count = 7
                demo_user.profile.save()

            # Seed 2 realistic past completed attempts for demo user if none exist
            if demo_user.quiz_attempts.count() == 0:
                self.seed_demo_attempts(demo_user)

        final_question_count = Question.objects.count()
        final_option_count = AnswerOption.objects.count()
        py_count = Question.objects.filter(topic__category__technology='PYTHON').count()
        dj_count = Question.objects.filter(topic__category__technology='DJANGO').count()

        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS(f"Seeding completed successfully!"))
        self.stdout.write(self.style.SUCCESS(f"Total Questions in Bank: {final_question_count}"))
        self.stdout.write(self.style.SUCCESS(f"  - Python Questions: {py_count}"))
        self.stdout.write(self.style.SUCCESS(f"  - Django Questions: {dj_count}"))
        self.stdout.write(self.style.SUCCESS(f"Total Answer Options: {final_option_count}"))
        self.stdout.write(self.style.SUCCESS("=" * 60))

    def seed_demo_attempts(self, user):
        """Creates sample test attempts for the demo user to visualize live dashboard analytics."""
        sample_questions = list(Question.objects.all().select_related('topic', 'topic__category').prefetch_related('options')[:20])
        if len(sample_questions) < 10:
            return

        # Attempt 1: Mock Interview
        attempt1 = QuizAttempt.objects.create(
            user=user,
            title="Full Technical Mock Interview #1",
            mode="MOCK_INTERVIEW",
            total_questions=10,
            correct_count=8,
            incorrect_count=2,
            unanswered_count=0,
            score=80.0,
            time_spent=640,
            time_limit=1200,
            status="COMPLETED",
            completed_at=timezone.now() - timezone.timedelta(days=2),
        )
        for idx, q in enumerate(sample_questions[:10], start=1):
            opts = list(q.options.all())
            correct_opt = next((o for o in opts if o.is_correct), opts[0])
            wrong_opt = next((o for o in opts if not o.is_correct), opts[0])
            # 8 correct, 2 incorrect
            selected = correct_opt if idx <= 8 else wrong_opt
            UserAnswer.objects.create(
                attempt=attempt1,
                question=q,
                selected_option=selected,
                is_correct=(selected == correct_opt),
                order_index=idx,
            )

        # Attempt 2: Advanced Django Drill
        attempt2 = QuizAttempt.objects.create(
            user=user,
            title="Django Advanced Architectural Exam",
            mode="EXAM",
            total_questions=10,
            correct_count=9,
            incorrect_count=1,
            unanswered_count=0,
            score=90.0,
            time_spent=510,
            time_limit=900,
            status="COMPLETED",
            completed_at=timezone.now() - timezone.timedelta(days=1),
        )
        for idx, q in enumerate(sample_questions[10:20], start=1):
            opts = list(q.options.all())
            correct_opt = next((o for o in opts if o.is_correct), opts[0])
            wrong_opt = next((o for o in opts if not o.is_correct), opts[0])
            selected = correct_opt if idx <= 9 else wrong_opt
            UserAnswer.objects.create(
                attempt=attempt2,
                question=q,
                selected_option=selected,
                is_correct=(selected == correct_opt),
                order_index=idx,
            )
