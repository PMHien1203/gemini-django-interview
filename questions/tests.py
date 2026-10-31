from django.test import TestCase, Client
from django.urls import reverse
from questions.models import Category, Topic, Question, AnswerOption

class QuestionsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat_py = Category.objects.create(
            name="Python Fundamentals",
            technology="PYTHON",
            slug="python-fundamentals"
        )
        self.topic_vars = Topic.objects.create(
            category=self.cat_py,
            name="Variables and Data Types",
            slug="variables-and-data-types"
        )

        self.q1 = Question.objects.create(
            topic=self.topic_vars,
            content="Is list mutable in Python?",
            difficulty="BEGINNER",
            explanation="Lists allow in-place mutations.",
            is_active=True
        )
        self.opt1 = AnswerOption.objects.create(question=self.q1, content="Yes", is_correct=True)
        self.opt2 = AnswerOption.objects.create(question=self.q1, content="No", is_correct=False)

        self.cat_dj = Category.objects.create(
            name="Django Architecture",
            technology="DJANGO",
            slug="django-architecture"
        )
        self.topic_mvt = Topic.objects.create(
            category=self.cat_dj,
            name="MVT Pattern",
            slug="mvt-pattern"
        )
        self.q2 = Question.objects.create(
            topic=self.topic_mvt,
            content="What does MVT stand for?",
            difficulty="ADVANCED",
            explanation="Model View Template.",
            is_active=True
        )
        AnswerOption.objects.create(question=self.q2, content="Model View Template", is_correct=True)
        AnswerOption.objects.create(question=self.q2, content="Multiple View Tasks", is_correct=False)

    def test_question_properties(self):
        """Test question string representation and correct option lookup."""
        self.assertIn("BEGINNER", str(self.q1))
        self.assertEqual(self.q1.correct_option, self.opt1)

    def test_question_filtering_by_technology(self):
        """Test filtering question bank by technology."""
        response = self.client.get(reverse('questions:list'), {'technology': 'PYTHON'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Is list mutable in Python?")
        self.assertNotContains(response, "What does MVT stand for?")

    def test_question_filtering_by_difficulty(self):
        """Test filtering question bank by difficulty."""
        response = self.client.get(reverse('questions:list'), {'difficulty': 'ADVANCED'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What does MVT stand for?")
        self.assertNotContains(response, "Is list mutable in Python?")

    def test_question_keyword_search(self):
        """Test keyword search in question bank."""
        response = self.client.get(reverse('questions:list'), {'q': 'mutable'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Is list mutable in Python?")

    def test_question_detail_view(self):
        """Test question detail page displays options and explanation."""
        response = self.client.get(reverse('questions:detail', args=[self.q1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lists allow in-place mutations.")
        self.assertContains(response, "Yes")
