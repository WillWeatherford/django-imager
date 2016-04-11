"""Test that Photo and Album models work as expected."""
from __future__ import unicode_literals
# from django.test import TestCase
from django.utils import timezone
from .models import Photo, Album
from imager_profile.tests import OneUserCase
import factory

PHOTO_TEST_BATCH_SIZE = 20
ALBUM_TEST_BATCH_SIZE = 5


class PhotoFactory(factory.django.DjangoModelFactory):
    """Creates Photo models for testing."""

    class Meta:
        """Assign Photo model as product of factory."""

        model = Photo


class AlbumFactory(factory.django.DjangoModelFactory):
    """Creates Album models for testing."""

    class Meta:
        """Assign Album model as product of factory."""

        model = Album


class OnePhotoOrAlbumCase(object):
    """Base case testing same named attributes of single Album or Photo."""

    def test_instance_exists(self):
        """Test that the instance set up from the factory does exist."""
        self.assertTrue(self.instance)

    def test_instance_pk(self):
        """Test that newly created User's profile has a primary key."""
        self.assertIsInstance(self.instance.pk, int)
        self.assertTrue(self.instance.pk)

    def test_instance_has_title(self):
        """Check that instance has its title attribute."""
        self.assertTrue(self.instance.title)

    def test_instance_has_desc(self):
        """Check that instance has its description attribute."""
        self.assertTrue(self.instance.description)

    def test_user(self):
        """Test that owner attr of Photo or Album is established User."""
        self.assertIs(self.instance.owner, self.user)


class OnePhotoCase(OneUserCase, OnePhotoOrAlbumCase):
    """Test case for a single Photo."""

    def setUp(self):
        """Add one Photo to the database for testing."""
        super(OnePhotoCase, self).setUp()

        self.instance = PhotoFactory.create(
            owner=self.user,
            title='Test title',
            description='Test description',
        )

    def test_photo_has_up_date(self):
        """Check that photo uploaded_date is a datetime before now."""
        self.assertGreater(timezone.now(), self.instance.date_uploaded)


class OneAlbumCase(OneUserCase, OnePhotoOrAlbumCase):
    """Test case for a single Album."""

    def setUp(self):
        """Add one Photo to the database for testing."""
        super(OneAlbumCase, self).setUp()

        self.instance = AlbumFactory.create(
            owner=self.user,
            title='Test title',
            description='Test description',
        )

    def test_album_has_created_date(self):
        """Check that photo uploaded_date is a datetime before now."""
        self.assertGreater(timezone.now(), self.instance.date_created)


class MultiPhotosAndAlbumsCase(OneUserCase):
    """Test case using many Photo instances."""

    def setUp(self):
        """Add many Photos to the database for testing."""
        super(MultiPhotosAndAlbumsCase, self).setUp()

        self.photo_batch = PhotoFactory.create_batch(
            PHOTO_TEST_BATCH_SIZE,
            owner=self.user,
            title='Test title',
            description='Test description',
        )
        self.album_batch = AlbumFactory.create_batch(
            ALBUM_TEST_BATCH_SIZE,
            owner=self.user,
            title='Test title',
            description='Test description',
        )

    def test_correct_photo_batch_size(self):
        """Test that batch of created photos are as many as expected."""
        self.assertEqual(len(self.photo_batch), PHOTO_TEST_BATCH_SIZE)

    def test_correct_album_batch_size(self):
        """Test that batch of created photos are as many as expected."""
        self.assertEqual(len(self.album_batch), ALBUM_TEST_BATCH_SIZE)

    def test_photo_owner(self):
        """Test that user attr of all Photos is established User."""
        for photo in self.photo_batch:
            self.assertIs(photo.owner, self.user)

    def test_album_owner(self):
        """Test that user attr of all Photos is established User."""
        for album in self.album_batch:
            self.assertIs(album.owner, self.user)
