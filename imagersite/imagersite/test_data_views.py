"""Tests for profile, library, album and photo views."""
from __future__ import unicode_literals
from django.test import Client, TestCase, override_settings
from django.contrib.auth.models import User
from imager_profile.tests import UserFactory
from imager_images.tests import TMP_MEDIA_ROOT, AlbumFactory, PhotoFactory
from .test_auth import user_from_response
from imager_images.models import Photo, Album

DEFAULT_IMG = 'media/django-magic.jpg'
HOME = '/'
REG = '/accounts/register/'
LOGIN = '/accounts/login/'
LOGOUT = '/accounts/logout/'
PROFILE = '/accounts/profile/'
LIBRARY = '/images/library/'
ALBUM = '/images/album/'
PHOTO = '/images/photo/'

NUM_USERS = 4
NUM_ALBUMS = 4
NUM_PHOTOS = 8


@override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
class AuthenticatedCase(TestCase):
    """Test case where we will fully register as part of setup."""

    def setUp(self):
        """Set up for unauthenticated case with no users."""
        self.users_sessions = []

        for user in UserFactory.create_batch(NUM_USERS):
            params = {'username': user.username, 'password': 'secret'}

            session = {'user': user}
            session['client'] = client = Client()
            session['login_response'] = client.post(LOGIN, params, follow=True)
            session['profile_response'] = client.get(
                PROFILE, params, follow=True)
            session['lib_response'] = client.get(LIBRARY, params, follow=True)
            self.users_sessions.append(session)

            album_batch = AlbumFactory.create_batch(NUM_ALBUMS, owner=user)
            for album in album_batch:
                photo_batch = PhotoFactory.create_batch(NUM_PHOTOS, owner=user)
                album.add_photos(photo_batch)

    def test_num_users(self):
        """Test there are as many users in the database as we registered."""
        self.assertEqual(User.objects.count(), NUM_USERS)

    def test_num_albums(self):
        """Test there are as many albums in the database as we created."""
        self.assertEqual(Album.objects.count(), NUM_USERS * NUM_ALBUMS)

    def test_num_photos(self):
        """Test there are as many users in the database as we created."""
        self.assertEqual(Photo.objects.count(),
                         NUM_USERS * NUM_ALBUMS * NUM_PHOTOS)

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
            response = session['lib_response']
            self.assertEqual(response.status_code, 200)

    def test_library_username(self):
        """Test that library page is accessible."""
        for session in self.users_sessions:
            response = session['lib_response']
            user = session['user']
            self.assertIn(user.username.encode('utf-8'), response.content)


    # test default image if no cover
    # test that owners see all of their albums
    # test that owners see all of their photos
    # test that owners don't see anyone elses's albums
    # test that owners don't see anyone else's photos
    # test that each album link from library can be clicked on (??)
    # test that each photo link in library and in album can be clicked on

