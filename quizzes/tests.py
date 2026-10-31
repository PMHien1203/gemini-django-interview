from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from questions.models import Category, Topic, Question, AnswerOption
from quizzes.models import QuizAttempt, UserAnswer
from quizzes.services import generate_quiz_attempt, submit_quiz_attempt, save_single_answer

class QuizzesTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='Password123!')
        self.user2 = User.objects.create_user(username='user2', password='Password123!')

        cat = Category.objects.create(name="Python Core", technology="PYTHON", slug="py-core")
        topic = Topic.objects.create(category=cat, name="Syntax", slug="syntax")

        # Create 3 test questions with 4 options each
        self.questions = []
        for i in range(1, 4):
            q = Question.objects.create(
                topic=topic,
                content=f"Question {i} test content",
                difficulty="INTERMEDIATE",
                explanation=f"Explanation for question {i}",
                is_active=True
            )
            # Create 1 correct, 3 wrong options
            opt_correct = AnswerOption.objects.create(question=q, content=f"Correct answer {i}", is_correct=True)
            opt_wrong1 = AnswerOption.objects.create(question=q, content=f"Wrong answer A {i}", is_correct=False)
            opt_wrong2 = AnswerOption.objects.create(question=q, content=f"Wrong answer B {i}", is_correct=False)
            opt_wrong3 = AnswerOption.objects.create(question=q, content=f"Wrong answer C {i}", is_correct=False)
            self.questions.append((q, opt_correct, opt_wrong1))

    def test_quiz_attempt_generation(self):
        """Test generating a quiz attempt for a user."""
        attempt = generate_quiz_attempt(
            user=self.user1,
            mode='EXAM',
            question_count=2,
            time_limit=600
        )
        self.assertEqual(attempt.user, self.user1)
        self.assertEqual(attempt.status, 'IN_PROGRESS')
        self.assertEqual(attempt.user_answers.count(), 2)

    def test_user_data_isolation_and_idor_prevention(self):
        """Test that user2 cannot access or submit user1's quiz attempt."""
        attempt = generate_quiz_attempt(user=self.user1, mode='EXAM', question_count=2)
        client = Client()
        client.force_login(self.user2)

        # Accessing user1's quiz page should return 403 Forbidden
        response = client.get(reverse('quizzes:take', args=[attempt.id]))
        self.assertEqual(response.status_code, 403)

        # Accessing user1's result page should return 403 Forbidden
        result_resp = client.get(reverse('quizzes:result', args=[attempt.id]))
        self.assertEqual(result_resp.status_code, 403)

    def test_single_answer_save_and_flag(self):
        """Test async saving of intermediate answer and review flag."""
        attempt = generate_quiz_attempt(user=self.user1, mode='EXAM', question_count=3)
        ua = attempt.user_answers.first()
        correct_opt = ua.question.options.filter(is_correct=True).first()

        # Save correct option
        updated_ua = save_single_answer(
            attempt=attempt,
            user=self.user1,
            question_id=ua.question_id,
            option_id=correct_opt.id,
            is_flagged=True
        )
        self.assertIsNotNone(updated_ua)
        self.assertEqual(updated_ua.selected_option, correct_opt)
        self.assertTrue(updated_ua.is_correct)
        self.assertTrue(updated_ua.is_flagged)

    def test_quiz_submission_and_backend_scoring(self):
        """Test that quiz submission calculates scores accurately on the backend."""
        attempt = generate_quiz_attempt(user=self.user1, mode='EXAM', question_count=3, time_limit=600)
        user_answers = list(attempt.user_answers.all())

        # Select correct for Q1, incorrect for Q2, leave Q3 unanswered
        q1 = user_answers[0].question
        q2 = user_answers[1].question
        opt_correct = q1.options.filter(is_correct=True).first()
        opt_wrong = q2.options.filter(is_correct=False).first()

        raw_answers = {
            str(q1.id): opt_correct.id,
            str(q2.id): opt_wrong.id,
        }

        completed_attempt = submit_quiz_attempt(
            attempt_id=attempt.id,
            user=self.user1,
            raw_answers_dict=raw_answers,
            elapsed_time_sec=120
        )

        self.assertEqual(completed_attempt.status, 'COMPLETED')
        self.assertEqual(completed_attempt.correct_count, 1)
        self.assertEqual(completed_attempt.incorrect_count, 1)
        self.assertEqual(completed_attempt.unanswered_count, 1)
        # 1/3 * 100 = 33.3%
        self.assertAlmostEqual(completed_attempt.score, 33.3, places=1)
        self.assertFalse(completed_attempt.is_passed)

    def test_prevent_duplicate_submissions(self):
        """Test that submitting an already completed attempt is idempotent and does not corrupt scores."""
        attempt = generate_quiz_attempt(user=self.user1, mode='EXAM', question_count=2)
        submit_quiz_attempt(attempt.id, self.user1, {}, 50)

        # Second submission
        second_attempt = submit_quiz_attempt(attempt.id, self.user1, {}, 90)
        self.assertEqual(second_attempt.status, 'COMPLETED')
        self.assertEqual(second_attempt.time_spent, 50) # Retains first completion metrics
