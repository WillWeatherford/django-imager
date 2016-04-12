"""Test that Photo and Album models work as expected."""
from __future__ import unicode_literals
from django.db.models.fields.files import ImageFieldFile
from django.test import TestCase, override_settings
from django.utils import timezone
from .models import Photo, Album, PUB_CHOICES
from imager_profile.tests import UserFactory
import factory
import random

PHOTO_BATCH_SIZE = 20
ALBUM_BATCH_SIZE = 10
USER_BATCH_SIZE = 5
TMP_MEDIA_ROOT = '/tmp/media/'


class PhotoFactory(factory.django.DjangoModelFactory):
    """Creates Photo models for testing."""

    class Meta:
        """Assign Photo model as product of factory."""

        model = Photo

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    published = random.choice(PUB_CHOICES)
    owner = factory.SubFactory(UserFactory, username='BestUser')
    img_file = factory.django.ImageField()


class AlbumFactory(factory.django.DjangoModelFactory):
    """Creates Album models for testing."""

    class Meta:
        """Assign Album model as product of factory."""

        model = Album

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    published = random.choice(PUB_CHOICES)
    owner = factory.SubFactory(UserFactory, username='BestUser')


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
        """Check that photo/album has its title attribute."""
        self.assertTrue(self.instance.title)

    def test_instance_has_desc(self):
        """Check that photo/album has its description attribute."""
        self.assertTrue(self.instance.description)

    def test_instance_has_mod_date(self):
        """Check that photo/album date_modified is a datetime before now."""
        self.assertGreater(timezone.now(), self.instance.date_modified)

    def test_instance_pub_date(self):
        """Check that photo/album date_published initializes as None."""
        self.assertIsNone(self.instance.date_published)

    def test_instance_published(self):
        """Check that photo/album published is in correct choices set."""
        self.assertIn(self.instance.published, PUB_CHOICES)


@override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
class OnePhotoCase(TestCase, OnePhotoOrAlbumCase):
    """Test case for a single Photo."""

    def setUp(self):
        """Add one Photo to the database for testing."""
        self.instance = PhotoFactory.create()

    def test_photo_has_up_date(self):
        """Check that photo uploaded_date is a datetime before now."""
        self.assertGreater(timezone.now(), self.instance.date_uploaded)

    def test_init_no_albums(self):
        """Check that Photo initializes with no albums."""
        self.assertFalse(self.instance.albums.count())

    def test_img_file(self):
        """Check that img_file exists."""
        self.assertTrue(self.instance.img_file)

    def test_img_file_type(self):
        """Check that img_file exists."""
        self.assertIsInstance(self.instance.img_file, ImageFieldFile)


@override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
class OneAlbumCase(TestCase, OnePhotoOrAlbumCase):
    """Test case for a single Album."""

    def setUp(self):
        """Add one Album to the database for testing."""
        self.instance = AlbumFactory.create()

    def test_init_no_photos(self):
        """Check that Album initializes with no photos."""
        self.assertFalse(self.instance.photos.count())

    def test_init_no_cover(self):
        """Check that Album initializes with no cover photo."""
        self.assertIs(self.instance.cover, None)

    def test_album_has_created_date(self):
        """Check that album date_created is a datetime before now."""
        self.assertGreater(timezone.now(), self.instance.date_created)


@override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
class ManyPhotosOneAlbumCase(TestCase):
    """Test case using many Photo instances and one Album."""

    def setUp(self):
        """Add one Album  and many Photos to the database for testing."""
        self.photo_batch = PhotoFactory.create_batch(PHOTO_BATCH_SIZE)
        self.album = AlbumFactory.create()
        self.album.add_photos(self.photo_batch)

    def test_correct_photo_batch_size(self):
        """Test that batch of created photos are as many as expected."""
        self.assertEqual(self.album.photos.count(), PHOTO_BATCH_SIZE)

    def test_photo_owner(self):
        """Test that user attr of all Photos is same User as Album."""
        for photo in self.photo_batch:
            self.assertEqual(photo.owner, self.album.owner)

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
        new_cover = self.album.photos.last()
        self.album.set_cover(new_cover)
        self.assertIsNot(self.album.cover, old_cover)
        self.assertIs(self.album.cover, new_cover)

    def test_cover_not_same_owner(self):
        """Test that a cover photo can be manually set."""
        new_photo = PhotoFactory(owner=UserFactory(username='OtherGuy'))
        with self.assertRaises(ValueError):
            self.album.set_cover(new_photo)

    def test_cover_not_same_album(self):
        """Test that a cover photo can be manually set."""
        new_photo = PhotoFactory(owner=self.album.owner)
        with self.assertRaises(KeyError):
            self.album.set_cover(new_photo)


@override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
class ManyPhotosManyAlbumsCase(TestCase):
    """Test case using many Photo and Album instances."""

    def setUp(self):
        """Add many Photos to the database for testing."""
        self.photo_batch = PhotoFactory.create_batch(PHOTO_BATCH_SIZE)
        self.album_batch = AlbumFactory.create_batch(ALBUM_BATCH_SIZE)
        for album in self.album_batch:
            album.add_photos(self.photo_batch)

    def gen_album_photo_comb(self):
        """Generate all album and photo combinations iteratively."""
        for album in self.album_batch:
            for photo in self.photo_batch:
                yield album, photo

    def test_correct_photo_batch_size(self):
        """Test that batch of created photos are as many as expected."""
        for album in self.album_batch:
            self.assertEqual(album.photos.count(), PHOTO_BATCH_SIZE)

    def test_correct_album_batch_size(self):
        """Test that batch of created albums are as many as expected."""
        for photo in self.photo_batch:
            self.assertEqual(photo.albums.count(), ALBUM_BATCH_SIZE)

    def test_album_photo_owner(self):
        """Test that all albums and photos have the same owner."""
        for album, photo in self.gen_album_photo_comb():
            self.assertEqual(album.owner, photo.owner)

    def test_multi_album(self):
        """Test that photos are in multiple albums, and vice versa."""
        for album in self.album_batch:
            for photo in album.photos.all():
                self.assertIn(photo, self.photo_batch)
        for photo in self.photo_batch:
            for album in photo.albums.all():
                self.assertIn(album, self.album_batch)

    def test_albums_in_photos_in_albums(self):
        """Test that all albums and photos are in each other."""
        for album, photo in self.gen_album_photo_comb():
            self.assertIn(album, photo.albums.all())
            self.assertIn(photo, album.photos.all())


@override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
class ManyPhotosManyAlbumsManyUsersCase(TestCase):
    """Establish full system test with many of each model."""

    def setUp(self):
        """Add many Photos to the database for testing."""
        self.photo_batch = []
        self.album_batch = []
        self.user_batch = UserFactory.create_batch(USER_BATCH_SIZE)
        for owner in self.user_batch:
            photo_batch = PhotoFactory.create_batch(
                PHOTO_BATCH_SIZE // USER_BATCH_SIZE,
                owner=owner)
            album_batch = AlbumFactory.create_batch(
                ALBUM_BATCH_SIZE // USER_BATCH_SIZE,
                owner=owner)
            for album in album_batch:
                album.add_photos(photo_batch)
            self.photo_batch.extend(photo_batch)
            self.album_batch.extend(album_batch)

    def test_all_owners_photos_size(self):
        """Test that all users have the expected number of photos."""
        for user in self.user_batch:
            self.assertEqual(user.photos.count(),
                             PHOTO_BATCH_SIZE // USER_BATCH_SIZE)

    def test_all_owners_albums_size(self):
        """Test that all users have the expected number of albums."""
        for user in self.user_batch:
            self.assertEqual(user.albums.count(),
                             ALBUM_BATCH_SIZE // USER_BATCH_SIZE)

    def test_exclusive_album_ownership(self):
        """Test that each user doesn't own other users' photos."""
        for user in self.user_batch:
            other_users = (other_user for other_user in self.user_batch
                           if other_user != user)
            for album in user.albums.all():
                for other_user in other_users:
                    self.assertNotIn(album, other_user.albums.all())

    def test_exclusive_photo_ownership(self):
        """Test that each user doesn't own other users' photos."""
        for user in self.user_batch:
            other_users = (other_user for other_user in self.user_batch
                           if other_user != user)
            for photo in user.photos.all():
                for other_user in other_users:
                    self.assertNotIn(photo, other_user.photos.all())

    def test_no_cover_other_owners(self):
        """Test that users cannot add other users photos as an album cover."""
        for user in self.user_batch:
            other_users = (other_user for other_user in self.user_batch
                           if other_user != user)
            album = user.albums.first()
            for other_user in other_users:
                other_photo = other_user.photos.first()
                with self.assertRaises(ValueError):
                    album.set_cover(other_photo)
