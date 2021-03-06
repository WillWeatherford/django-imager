"""Tests for root config views and urls."""
from __future__ import unicode_literals
from django.core import mail
from django.test import Client, TestCase
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm
import re

DEFAULT_IMG = 'media/django-magic.jpg'
HOME = '/'
REG = '/accounts/register/'
LOGIN = '/accounts/login/'
LOGOUT = '/accounts/logout/'
PROFILE = '/profile/'
LIBRARY = '/images/library/'

BAD_LOGIN_PARAMS = {'username': 'NotRealUser', 'password': 'notsecret'}
BAD_REG_PARAMS = {'username': 'NotRealUser',
                  'email': 'bademail@baddomain',
                  'password1': 'short',
                  'password2': 'shrt'}

GOOD_REG_PARAMS = {'username': 'CoolPerson',
                   'email': 'coolperson@example.com',
                   'password1': 's00p3rs3cr3t',
                   'password2': 's00p3rs3cr3t'}

LINK_PATTERN = r'/accounts/activate/.*/'


def user_from_response(response):
    """Helper function to dig the user from the HTTPresponse."""
    for dic in response.context[0]:
        user = dic.get('user')
        if user:
            break
    return user


class UnauthenticatedCase(TestCase):
    """Testing when user is not logged in."""

    def setUp(self):
        """Set up for unauthenticated case with no users."""
        client = Client()
        self.home_response = client.get(HOME)
        self.reg_response = client.get(REG)
        self.reg_post_bad = client.post(REG, BAD_REG_PARAMS)
        self.login_get_response = client.get(LOGIN)
        self.login_post_bad = client.post(LOGIN, BAD_LOGIN_PARAMS)
        self.logout_response = client.get(LOGOUT)
        self.profile_response = client.get(PROFILE)
        self.library_response = client.get(LIBRARY)

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
        self.assertEqual(self.logout_response.status_code, 200)

    def test_register_ok(self):
        """Check that register page can be visited."""
        self.assertEqual(self.reg_response.status_code, 200)

    def test_no_authenticated_user(self):
        """Test that there is no authenticated user."""
        user = user_from_response(self.home_response)
        self.assertFalse(user.is_authenticated())

    def test_no_username_display(self):
        """Test that message displaying username does not appear."""
        self.assertNotIn(b'Log out', self.home_response.content)

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

    def test_login_failure_ok(self):
        """Test that login failure returns to login page."""
        self.assertEqual(self.login_post_bad.status_code, 200)

    def test_login_failure_message(self):
        """Test that login fails since there are no registered users."""
        expected_msg = b'Please enter a correct username and password.'
        self.assertIn(expected_msg, self.login_post_bad.content)

    def test_reg_failure_ok(self):
        """Test that bad registration information returns a 200 response."""
        self.assertEqual(self.reg_post_bad.status_code, 200)

    def test_reg_failure_message_email(self):
        """Test that bad registration gives a bad email message."""
        expected_msg = b'Enter a valid email address.'
        self.assertIn(expected_msg, self.reg_post_bad.content)

    def test_reg_failure_message_password_match(self):
        """Test bad registration gives message when passwords don't match."""
        expected_msg = b'The two password fields didn&#39;t match.'
        self.assertIn(expected_msg, self.reg_post_bad.content)

    def test_profile_login_required(self):
        """Test that getting /accounts/profile/ redirects to login."""
        self.assertEqual(self.profile_response.status_code, 302)
        self.assertTrue(self.profile_response.url.startswith(LOGIN))

    def test_library_login_required(self):
        """Test that getting /images/library/ redirects to login."""
        self.assertEqual(self.profile_response.status_code, 302)
        self.assertTrue(self.profile_response.url.startswith(LOGIN))


class RegistrationCase(TestCase):
    """Tests with one registraton post attempt in setup."""

    def setUp(self):
        """Set up for unauthenticated case with no users."""
        self.client = Client()
        self.reg_post_good = self.client.post(REG, GOOD_REG_PARAMS,
                                              follow=True)
        try:
            self.email = mail.outbox[0]
        except IndexError:
            self.email = None

    def tearDown(self):
        """Delete all users to re-use good params."""
        for user in User.objects.all():
            user.delete()

    def test_user_in_db(self):
        """Test that there is one user in the database."""
        self.assertEqual(User.objects.count(), 1)

    def test_user_in_db_inactive(self):
        """Test that there is one user in the database, who is inactive."""
        self.assertFalse(User.objects.first().is_active)

    def test_good_registration_ok(self):
        """Test that good registration gives a redirect response."""
        self.assertEqual(self.reg_post_good.status_code, 200)

    def test_good_registration_redirect(self):
        """Test that good registration redirects through complete page."""
        self.assertIn(('/accounts/register/complete/', 302),
                      self.reg_post_good.redirect_chain)

    def test_reg_email_sent(self):
        """Test that the activation email is in the outbox."""
        self.assertTrue(self.email)

    def test_reg_email_to(self):
        """Test that the activation email was sent to registered email."""
        self.assertIn(GOOD_REG_PARAMS['email'], self.email.to)

    def test_reg_email_link(self):
        """Test that activation email has an activation link in the body."""
        self.assertTrue(re.search(LINK_PATTERN, self.email.body))

    def test_get_activation_link_ok(self):
        """Test that link from activation email works."""
        path = re.search(LINK_PATTERN, self.email.body).group()
        response = self.client.get(path, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_activation_link_redirect(self):
        """Test that link from activation email works."""
        path = re.search(LINK_PATTERN, self.email.body).group()
        response = self.client.get(path, follow=True)
        self.assertIn(('/accounts/activate/complete/', 302),
                      response.redirect_chain)


class AuthenticatedCase(TestCase):
    """Test case where we will fully register as part of setup."""

    def setUp(self):
        """Set up for unauthenticated case with no users."""
        self.client = Client()
        self.client.post(REG, GOOD_REG_PARAMS, follow=True)
        try:
            email = mail.outbox[0]
            path = re.search(LINK_PATTERN, email.body).group()
            self.client.get(path, follow=True)
        except IndexError:
            email = None
        self.user = User.objects.first()
        params = {'username': self.user.username,
                  'password': BAD_REG_PARAMS['password1']}
        self.login_post_bad = self.client.post(LOGIN, params, follow=True)
        params['password'] = GOOD_REG_PARAMS['password1']
        self.login_post_good = self.client.post(LOGIN, params, follow=True)

    def tearDown(self):
        """Delete all users to re-use good params."""
        self.user.delete()

    def test_user_in_db(self):
        """Test that there is one user in the database."""
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first(), self.user)

    def test_user_in_db_active(self):
        """Test that the user is active."""
        self.assertTrue(self.user.is_active)

    def test_user_in_db_params(self):
        """Test that the user in the database has the expected info."""
        self.assertEqual(self.user.username, GOOD_REG_PARAMS['username'])
        self.assertEqual(self.user.email, GOOD_REG_PARAMS['email'])

    def test_unique_reg_fail(self):
        """Test that we cannot re-register with the same username."""
        response = self.client.post(REG, GOOD_REG_PARAMS)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A user with that username already exists.',
                      response.content)

    def test_login_bad_password_ok(self):
        """Test that bad password login attempt returns login page OK."""
        self.assertEqual(self.login_post_bad.status_code, 200)

    def test_login_bad_password_message(self):
        """Test that bad password login attempt returns login page OK."""
        expected_msg = b'Please enter a correct username and password.'
        self.assertIn(expected_msg, self.login_post_bad.content)

    def test_login_bad_password_unauthenticated(self):
        """Test that bad password login attempt returns login page OK."""
        user = user_from_response(self.login_post_bad)
        self.assertIsInstance(user, AnonymousUser)

    def test_login_post_good_ok(self):
        """Test that registered user can log in."""
        self.assertEqual(self.login_post_good.status_code, 200)

    def test_login_post_good_authenticated_user(self):
        """Test that there is an authenticated user in response."""
        user = user_from_response(self.login_post_good)
        self.assertIsInstance(user, User)

    def test_logged_in_logout_link(self):
        """Test that logged in user sees logout link."""
        self.assertIn(b'Log out', self.login_post_good.content)
