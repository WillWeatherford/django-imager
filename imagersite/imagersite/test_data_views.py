"""Tests for profile, library, album and photo views."""
from __future__ import unicode_literals
from django.test import Client, TestCase
from django.contrib.auth.models import AnonymousUser, User
from imager_profile.tests import UserFactory
from .test_auth import user_from_response

DEFAULT_IMG = 'media/django-magic.jpg'
HOME = '/'
REG = '/accounts/register/'
LOGIN = '/accounts/login/'
LOGOUT = '/accounts/logout/'
PROFILE = '/accounts/logout/'
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
        self.client = Client()
        self.user_batch = UserFactory.create_batch(NUM_USERS)

        for user in self.user_batch:
            params = {'username': user.username, 'password': 'secret'}
            response = self.client.post(LOGIN, params, follow=True)
            setattr(self, '{}_response'.format(user.username), response)

    def test_num_users(self):
        """Test there are as many users in the database as we registered."""
        self.assertEqual(User.objects.count(), NUM_USERS)

    def test_all_logged_in(self):
        """Test that all users are logged in."""
        for user in self.user_batch:
            response = getattr(self, '{}_response'.format(user.username))
            context_user = user_from_response(response)
            self.assertEqual(user, context_user)
            self.assertTrue(user.is_authenticated())
            self.assertTrue(context_user.is_authenticated())


    # test default image if no cover
    # test that owners see all of their albums
    # test that owners see all of their photos
    # test that owners don't see anyone elses's albums
    # test that owners don't see anyone else's photos
    # test that each album link from library can be clicked on (??)
    # test that each photo link in library and in album can be clicked on

