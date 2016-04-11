"""Test that Photo and Album models work as expected."""
from __future__ import unicode_literals
from django.test import TestCase
from django.utils import timezone
from .models import Photo, Album
from imager_profile.tests import UserFactory
import factory

PHOTO_TEST_BATCH_SIZE = 20
ALBUM_TEST_BATCH_SIZE = 5


class PhotoFactory(factory.django.DjangoModelFactory):
    """Creates Photo models for testing."""

    class Meta:
        """Assign Photo model as product of factory."""

        model = Photo

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    published = 'private'


class AlbumFactory(factory.django.DjangoModelFactory):
    """Creates Album models for testing."""

    class Meta:
        """Assign Album model as product of factory."""

        model = Album

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    published = 'private'


class OnePhotoOrAlbumCase(object):
    """Base case testing same named attributes of single Album or Photo."""

    def test_instance_exists(self):
        """Test that the instance set up from the factory does exist."""
        self.assertTrue(self.instance)

    def test_instance_pk(self):
        """Test that new Album or Photo has an integer primary key."""
        self.assertIsInstance(self.instance.pk, int)
        self.assertTrue(self.instance.pk)

    def test_instance_has_title(self):
        """Check that instance has its title attribute."""
        self.assertTrue(self.instance.title)

    def test_instance_has_desc(self):
        """Check that instance has its description attribute."""
        self.assertTrue(self.instance.description)

    def test_owner(self):
        """Test that owner attr of Photo or Album is established User."""
        self.assertIs(self.instance.owner, self.user)

    def test_instance_has_mod_date(self):
        """Check that photo date_modified is a datetime before now."""
        self.assertGreater(timezone.now(), self.instance.date_modified)

    def test_instance_has_pub_date(self):
        """Check that photo date_modified is a datetime before now."""
        self.assertGreater(timezone.now(), self.instance.date_published)


class OnePhotoCase(TestCase, OnePhotoOrAlbumCase):
    """Test case for a single Photo."""

    def setUp(self):
        """Add one Photo to the database for testing."""
        self.user = UserFactory.create()
        self.instance = PhotoFactory.create(owner=self.user)

    def test_photo_has_up_date(self):
        """Check that photo uploaded_date is a datetime before now."""
        self.assertGreater(timezone.now(), self.instance.date_uploaded)

    def test_init_no_albums(self):
        """Check that Photo initializes with no albums."""
        self.assertFalse(self.instance.albums.count())


class OneAlbumCase(TestCase, OnePhotoOrAlbumCase):
    """Test case for a single Album."""

    def setUp(self):
        """Add one Album to the database for testing."""
        self.user = UserFactory.create()
        self.instance = AlbumFactory.create(owner=self.user)

    def test_init_no_photos(self):
        """Check that Album initializes with no photos."""
        self.assertFalse(self.instance.photos.count())

    def test_init_no_cover(self):
        """Check that Album initializes with no cover photo."""
        self.assertIs(self.instance.cover, None)

    def test_album_has_created_date(self):
        """Check that album date_created is a datetime before now."""
        self.assertGreater(timezone.now(), self.instance.date_created)


class MultiPhotosAndAlbumsCase(TestCase):
    """Test case using many Photo instances."""

    def setUp(self):
        """Add many Photos to the database for testing."""
        self.user = UserFactory.create()
        self.photo_batch = PhotoFactory.create_batch(
            PHOTO_TEST_BATCH_SIZE,
            owner=self.user)
        self.album_batch = AlbumFactory.create_batch(
            ALBUM_TEST_BATCH_SIZE,
            owner=self.user)

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

    def test_set_one_album(self):
        """Test that photo batch  added to album have correct relationship."""
        album = self.album_batch[0]
        album.add_photos(self.photo_batch)
        for photo in self.photo_batch:
            self.assertIn(album, photo.albums.all())
            self.assertIn(photo, album.photos.all())

    def test_multi_albums(self):
        """Test that photos can be in multiple albums."""
        for album in self.album_batch:
            album.add_photos(self.photo_batch)
            self.assertEqual(list(album.photos.all()), self.photo_batch)
        for photo in self.photo_batch:
            self.assertEqual(list(photo.albums.all()), self.album_batch)
