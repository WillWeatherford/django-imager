"""Tests for profile, library, album and photo views."""
from __future__ import unicode_literals
from django.core import mail
from django.test import Client, TestCase
from django.contrib.auth.models import AnonymousUser, User
import re

DEFAULT_IMG = 'media/django-magic.jpg'
HOME = '/'
REG = '/accounts/register/'
LOGIN = '/accounts/login/'
LOGOUT = '/accounts/logout/'
PROFILE = '/accounts/logout/'
LIBRARY = '/images/library/'
ALBUM = '/images/album/'
PHOTO = '/images/photo/'

# import userfactory instead
# import photofactory

GOOD_REG_PARAMS = {'username': 'CoolPerson{}',
                   'email': 'coolperson{}@example.com',
                   'password1': 's00p3rs3cr3t',
                   'password2': 's00p3rs3cr3t'}

NUM_USERS = 3

LINK_PATTERN = r'/accounts/activate/.*/'


class AuthenticatedCase(TestCase):
    """Test case where we will fully register as part of setup."""

    def setUp(self):
        """Set up for unauthenticated case with no users."""
        self.client = Client()
        for n in range(NUM_USERS):
            params = GOOD_REG_PARAMS.copy()
            params['username'] = params['username'].format(n)
            params['email'] = params['email'].format(n)
            self.client.post(REG, params, follow=True)
            email = mail.outbox[0]
            path = re.search(LINK_PATTERN, email.body).group()
            self.client.get(path, follow=True)
            user = User.objects.get(username=params['username'])
            setattr(self, 'user' + str(n), user)
            self.login_post_good = self.client.post(LOGIN, params, follow=True)

    def test_num_users(self):
        """Test there are as many users in the database as we registered."""
        self.assertEqual(User.objects.count(), NUM_USERS)

