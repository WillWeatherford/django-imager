"""Test that Photo and Album models work as expected."""
from __future__ import unicode_literals
from django.test import TestCase
from django.utils import timezone
from .models import Photo, Album, PUB_CHOICES
from imager_profile.tests import UserFactory
import factory
import random

PHOTO_TEST_BATCH_SIZE = 20
ALBUM_TEST_BATCH_SIZE = 5


class PhotoFactory(factory.django.DjangoModelFactory):
    """Creates Photo models for testing."""

    class Meta:
        """Assign Photo model as product of factory."""

        model = Photo

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    published = random.choice(PUB_CHOICES)


class AlbumFactory(factory.django.DjangoModelFactory):
    """Creates Album models for testing."""

    class Meta:
        """Assign Album model as product of factory."""

        model = Album

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    published = random.choice(PUB_CHOICES)


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
        self.user.set_password('secret')
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
        self.user.set_password('secret')
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


class ManyPhotosOneAlbumCase(TestCase):
    """Test case using many Photo instances and one Album."""

    def setUp(self):
        """Add one Album  and many Photos to the database for testing."""
        self.user = UserFactory.create()
        self.user.set_password('secret')
        self.photo_batch = PhotoFactory.create_batch(
            PHOTO_TEST_BATCH_SIZE,
            owner=self.user)
        self.album = AlbumFactory.create(owner=self.user)
        self.album.add_photos(self.photo_batch)

    def test_correct_photo_batch_size(self):
        """Test that batch of created photos are as many as expected."""
        self.assertEqual(len(self.album.photos.all()), PHOTO_TEST_BATCH_SIZE)

    def test_photo_owner(self):
        """Test that user attr of all Photos is same User as Album."""
        for photo in self.photo_batch:
            self.assertIs(photo.owner, self.album.owner)

    def test_photos_owner(self):
        """Test that user attr of album.photos is same User as album."""
        for photo in self.album.photos.all():
            self.assertEqual(photo.owner, self.album.owner)

    def test_album_photos_relationship(self):
        """Test that photo batch  added to album have correct relationship."""
        for photo in self.photo_batch:
            self.assertIn(self.album, photo.albums.all())
            self.assertIn(photo, self.album.photos.all())

    def test_cover_photo_auto_set(self):
        """Test that a cover photo is set when photos have been added."""
        self.assertIsNotNone(self.album.cover)

    def test_cover_photo_manual_set(self):
        """Test that a cover photo can be manually set."""
        old_cover = self.album.cover
        new_cover = list(self.album.photos.all())[-1]
        self.album.set_cover(new_cover)
        self.assertIsNot(self.album.cover, old_cover)
        self.assertIs(self.album.cover, new_cover)


class ManyPhotosManyAlbumsCase(TestCase):
    """Test case using many Photo and Album instances."""

    def setUp(self):
        """Add many Photos to the database for testing."""
        self.user = UserFactory.create()
        self.photo_batch = PhotoFactory.create_batch(
            PHOTO_TEST_BATCH_SIZE,
            owner=self.user)
        self.album_batch = AlbumFactory.create_batch(
            ALBUM_TEST_BATCH_SIZE,
            owner=self.user)
        for album in self.album_batch:
            album.add_photos(self.photo_batch)

    def gen_album_photo_comb(self):
        """Generate all album and photo combinations iteratively."""
        for album in self.album_batch:
            for photo in self.photo_batch:
                yield album, photo

    def test_correct_album_batch_size(self):
        """Test that batch of created photos are as many as expected."""
        photo = self.photo_batch[0]
        self.assertEqual(len(list(photo.albums.all())), ALBUM_TEST_BATCH_SIZE)

    def test_album_owner(self):
        """Test that user attr of all Photos is established User."""
        for album in self.album_batch:
            self.assertIs(album.owner, self.user)

    def test_album_photo_owner(self):
        """Test that all albums and photos have the same owner."""
        for album, photo in self.gen_album_photo_comb():
            self.assertIs(album.owner, photo.owner)

    def test_multi_album(self):
        """Test that photos are in multiple albums, and vice versa."""
        for album in self.album_batch:
            self.assertEqual(list(album.photos.all()), self.photo_batch)
        for photo in self.photo_batch:
            self.assertEqual(list(photo.albums.all()), self.album_batch)

    def test_albums_in_photos_in_albums(self):
        """Test that all albums and photos are in each other."""
        for album, photo in self.gen_album_photo_comb():
            self.assertIn(album, photo.albums.all())
            self.assertIn(photo, album.photos.all())


# Test with multi owners - no overlap of photo sets
# Test error raised when trying to set cover wrong
