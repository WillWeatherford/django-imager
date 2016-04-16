"""Tests for profile, library, album and photo views."""
from __future__ import unicode_literals
from django.test import Client, TestCase
from django.contrib.auth.models import User
from imager_profile.tests import UserFactory
from .test_auth import user_from_response

DEFAULT_IMG = 'media/django-magic.jpg'
HOME = '/'
REG = '/accounts/register/'
LOGIN = '/accounts/login/'
LOGOUT = '/accounts/logout/'
PROFILE = '/accounts/profile/'
LIBRARY = '/images/library/'
ALBUM = '/images/album/'
PHOTO = '/images/photo/'

# import photofactory

# GOOD_REG_PARAMS = {'username': 'CoolPerson{}',
#                    'email': 'coolperson{}@example.com',
#                    'password1': 's00p3rs3cr3t',
#                    'password2': 's00p3rs3cr3t'}

NUM_USERS = 3

# LINK_PATTERN = r'/accounts/activate/.*/'


class AuthenticatedCase(TestCase):
    """Test case where we will fully register as part of setup."""

    def setUp(self):
        """Set up for unauthenticated case with no users."""
        self.user_batch = UserFactory.create_batch(NUM_USERS)
        self.users_sessions = []

        for user in self.user_batch:
            client = Client()
            params = {'username': user.username, 'password': 'secret'}
            response = client.post(LOGIN, params, follow=True)
            session = {'user': user, 'client': client, 'login_response': response}
            self.users_sessions.append(session)

    def test_num_users(self):
        """Test there are as many users in the database as we registered."""
        self.assertEqual(User.objects.count(), NUM_USERS)

    def test_all_logged_in(self):
        """Test that all users are logged in."""
        for session in self.users_sessions:
            user = session['user']
            context_user = user_from_response(session['login_response'])
            self.assertEqual(user, context_user)
            self.assertTrue(user.is_authenticated())
            self.assertTrue(context_user.is_authenticated())

    def test_login_to_profile(self):
        """Test that response has redirected to profile page."""
        for session in self.users_sessions:
            login_response = session['login_response']
            self.assertEqual(login_response.status_code, 200)
            self.assertEqual(login_response.request['PATH_INFO'], PROFILE)

    def test_library_ok(self):
        """Test that library page is accessible."""
        for session in self.users_sessions:
            client = session['client']
            response = client.get('/images/library/')
            self.assertEqual(response.status_code, 200)

    def test_library_ok(self):
        """Test that library page is accessible."""
        for session in self.users_sessions:
            client = session['client']
            response = client.get('/images/library/')
            self.assertEqual(response.status_code, 200)


    # test that library page is accessible
    # test default image if no cover
    # test that owners see all of their albums
    # test that owners see all of their photos
    # test that owners don't see anyone elses's albums
    # test that owners don't see anyone else's photos
    # test that each album link from library can be clicked on (??)
    # test that each photo link in library and in album can be clicked on

