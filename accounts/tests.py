from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='pydeveloper',
            email='dev@example.com',
            password='ComplexPassword123!',
            first_name='Alex',
            last_name='Dev'
        )

    def test_user_profile_auto_created(self):
        """Test that UserProfile is automatically provisioned via signal upon user creation."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.target_role, 'mid')

    def test_user_registration(self):
        """Test user registration flow."""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newcoder',
            'email': 'newcoder@example.com',
            'first_name': 'New',
            'last_name': 'Coder',
            'target_role': 'senior',
            'experience_level': 'ADVANCED',
            'password': 'PasswordSecure2026!',
            'password_confirm': 'PasswordSecure2026!',
        })
        self.assertEqual(response.status_code, 302) # Redirect to dashboard
        new_user = User.objects.get(username='newcoder')
        self.assertEqual(new_user.profile.target_role, 'senior')

    def test_user_login_and_logout(self):
        """Test login with valid and invalid credentials and logout."""
        # Invalid login
        bad_response = self.client.post(reverse('accounts:login'), {
            'username': 'pydeveloper',
            'password': 'wrongpassword'
        })
        self.assertEqual(bad_response.status_code, 200)

        # Valid login
        good_response = self.client.post(reverse('accounts:login'), {
            'username': 'pydeveloper',
            'password': 'ComplexPassword123!'
        })
        self.assertEqual(good_response.status_code, 302)

        # Logout
        logout_response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(logout_response.status_code, 302)

    def test_demo_login(self):
        """Test the one-click demo login route."""
        response = self.client.get(reverse('accounts:demo_login'))
        self.assertEqual(response.status_code, 302)
        demo_user = User.objects.get(username='demo_developer')
        self.assertIsNotNone(demo_user)

    def test_profile_update_and_protection(self):
        """Test profile page access control and updating profile attributes."""
        # Unauthenticated redirect to login
        unauth_resp = self.client.get(reverse('accounts:profile'))
        self.assertEqual(unauth_resp.status_code, 302)

        # Authenticated access
        self.client.force_login(self.user)
        auth_resp = self.client.get(reverse('accounts:profile'))
        self.assertEqual(auth_resp.status_code, 200)

        # Post update
        update_resp = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Alexander',
            'last_name': 'Developer',
            'email': 'alex.dev@example.com',
            'target_role': 'senior',
            'experience_level': 'ADVANCED',
            'preferred_theme': 'light',
            'bio': 'Passionate about backend architectures.'
        })
        self.assertEqual(update_resp.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Alexander')
        self.assertEqual(self.user.profile.target_role, 'senior')
        self.assertEqual(self.user.profile.preferred_theme, 'light')
