"""Tests for profile, library, album and photo views."""
from __future__ import unicode_literals
from django.test import Client, TestCase, override_settings
from django.contrib.auth.models import User
from imager_profile.tests import UserFactory
from imager_images.tests import TMP_MEDIA_ROOT, AlbumFactory, PhotoFactory
from .test_auth import user_from_response
from imager_images.models import Photo, Album
import re

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

NUM_PAT = r'(?P<num>[0-9])'
FRIENDS_PAT = NUM_PAT + r' friends'
ALBUMS_PAT = NUM_PAT + r' albums'
PHOTOS_PAT = NUM_PAT + r' photos'


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
            ctx_user = user_from_response(session['login_response'])
            self.assertEqual(user, ctx_user)
            self.assertTrue(user.is_authenticated())
            self.assertTrue(ctx_user.is_authenticated())

    def test_login_to_profile(self):
        """Test that response has redirected to profile page."""
        for session in self.users_sessions:
            login_response = session['login_response']
            self.assertEqual(login_response.status_code, 200)
            self.assertEqual(login_response.request['PATH_INFO'], PROFILE)

    def test_profile_ok(self):
        """Test that user can access profile ok."""
        for session in self.users_sessions:
            response = session['profile_response']
            self.assertEqual(response.status_code, 200)

    def test_profile_username(self):
        """Test that user sees their username on profile page."""
        for session in self.users_sessions:
            response = session['profile_response']
            user = session['user']
            self.assertIn(user.username.encode('utf-8'), response.content)

    def test_friends_count_profile(self):
        """Test user sees correct number of friends on profile page."""
        for session in self.users_sessions:
            response = session['profile_response']
            user = session['user']
            match = re.search(FRIENDS_PAT, response.content.decode('utf-8'))
            num = int(match.groupdict()['num'])
            self.assertEqual(user.profile.friends.count(), num)

    def test_photos_count_profile(self):
        """Test user sees correct number of photos on profile page."""
        for session in self.users_sessions:
            response = session['profile_response']
            user = session['user']
            match = re.search(PHOTOS_PAT, response.content.decode('utf-8'))
            self.assertEqual(user.photos.count(), int(match.groupdict()['num']))

    def test_albums_count_profile(self):
        """Test user sees correct number of albums on profile page."""
        for session in self.users_sessions:
            response = session['profile_response']
            user = session['user']
            match = re.search(ALBUMS_PAT, response.content.decode('utf-8'))
            self.assertEqual(user.albums.count(), int(match.groupdict()['num']))

    def test_library_ok(self):
        """Test that library page is accessible."""
        for session in self.users_sessions:
            response = session['lib_response']
            self.assertEqual(response.status_code, 200)

    def test_library_username(self):
        """Test that the user sees their username on library page."""
        for session in self.users_sessions:
            response = session['lib_response']
            user = session['user']
            self.assertIn(user.username.encode('utf-8'), response.content)

    def test_library_albums(self):
        """Test that all of user's album's titles display in library."""
        for session in self.users_sessions:
            response = session['lib_response']
            user = session['user']
            ctx_user = user_from_response(response)
            for album in user.albums.all():
                self.assertIn(album, ctx_user.albums.all())

    def test_library_photos(self):
        """Test that all of user's album's titles display in library."""
        for session in self.users_sessions:
            response = session['lib_response']
            user = session['user']
            ctx_user = user_from_response(response)
            for photo in user.photos.all():
                self.assertIn(photo, ctx_user.photos.all())

    def test_only_user_albums(self):
        """Test that only user's album's titles display in library."""
        for session in self.users_sessions:
            response = session['lib_response']
            other_users = (ses['user'] for ses in self.users_sessions
                           if ses != session)
            ctx_user = user_from_response(response)
            for album in ctx_user.albums.all():
                for other in other_users:
                    self.assertNotIn(album, other.albums.all())

    def test_only_user_photos(self):
        """Test that all of user's album's titles display in library."""
        for session in self.users_sessions:
            response = session['lib_response']
            other_users = (ses['user'] for ses in self.users_sessions
                           if ses != session)
            ctx_user = user_from_response(response)
            for photo in ctx_user.photos.all():
                for other in other_users:
                    self.assertNotIn(photo, other.photos.all())

    def test_album_page(self):
        """Test that every album page can be reached by get."""
        for session in self.users_sessions:
            user = session['user']
            client = session['client']
            for album in user.albums.all():
                response = client.get(album.get_url())
                self.assertEqual(response.status_code, 200)

    def test_photo_page(self):
        """Test that every photo page can be reached by get."""
        for session in self.users_sessions:
            user = session['user']
            client = session['client']
            for photo in user.photos.all():
                response = client.get(photo.get_url())
                self.assertEqual(response.status_code, 200)
