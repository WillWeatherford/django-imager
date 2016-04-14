"""Tests for root config views and urls."""
from __future__ import unicode_literals
from django.test import Client, TestCase
from django.contrib.auth.models import AnonymousUser, User
from registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm

DEFAULT_IMG = 'media/django-magic.jpg'


class UnauthenticatedCase(TestCase):
    """Testing when user is not logged in."""

    def setUp(self):
        """Set up for simple unauthenticated case with no users."""
        self.client = Client()
        self.home_response = self.client.get('/')
        self.reg_response = self.client.get('/accounts/register/')
        self.login_get_response = self.client.get('/accounts/login/')
        params = {'username': 'NotRealUser', 'password': 'notsecret'}
        self.login_post_response = self.client.post('/accounts/login/', params)
        self.home_context = self.home_response.context[0]

    def test_no_users_in_db(self):
        """Make sure test session starts with empty database."""
        self.assertFalse(User.objects.count())

    def test_homepage_ok(self):
        """Check that homepage can be visited."""
        self.assertEqual(self.home_response.status_code, 200)

    def test_login_ok(self):
        """Check that login page can be visited."""
        self.assertEqual(self.login_get_response.status_code, 200)

    def test_logout_ok(self):
        """Check that logout page can be visited."""
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)

    def test_register_ok(self):
        """Check that register page can be visited."""
        self.assertEqual(self.reg_response.status_code, 200)

    def test_no_authenticated_user(self):
        """Test that there is no authenticated user."""
        for dic in self.home_context:
            try:
                user = dic['user']
                break
            except KeyError:
                pass
        self.assertIsInstance(user, AnonymousUser)

    def test_no_username_display(self):
        """Test that message displaying username does not appear."""
        self.assertFalse(b'Log out' in self.home_response.content)

    def test_default_img(self):
        """Check that the default image is displayed, not a user's image."""
        img_url = self.home_response.context_data.get('img_url')
        self.assertEqual(img_url, DEFAULT_IMG)

    def test_correct_reg_form(self):
        """Check that the registration page delivers the registration form."""
        self.assertIsInstance(self.reg_response.context_data.get('form'),
                              RegistrationForm)

    def test_correct_login_form(self):
        """Check that the login page delivers the registration form."""
        self.assertIsInstance(self.login_get_response.context_data.get('form'),
                              AuthenticationForm)

    def test_login_failure_message(self):
        """Test that login fails since there are no registered users."""
        expected_msg = b'Please enter a correct username and password.'
        self.assertIn(expected_msg, self.login_post_response.content)

    def test_login_failure_ok(self):
        """Test that login fails since there are no registered users."""
        self.assertEqual(self.login_post_response.status_code, 200)
