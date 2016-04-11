"""Test that Photo and Album models work as expected."""
from __future__ import unicode_literals
# from django.test import TestCase
from django.utils import timezone
from .models import Photo
from imager_profile.tests import OneUserCase
import factory

PHOTO_TEST_BATCH_SIZE = 20


class PhotoFactory(factory.django.DjangoModelFactory):
    """Creates Photo models for testing."""

    class Meta:
        """Assign Photo model as product of factory."""

        model = Photo


class BasicPhotoCase(OneUserCase):
    """Simple test case for Photos."""

    def setUp(self):
        """Add one Photo to the database for testing."""
        super(BasicPhotoCase, self).setUp()

        self.photo = PhotoFactory.create(
            user=self.user,
            title='Test photo',
            description='Test description',
        )

    def test_photo_exists(self):
        """Test that the photo set up from the factory does exist."""
        self.assertTrue(self.photo)

    def test_photo_pk(self):
        """Test that newly created User's profile has a primary key."""
        self.assertIsInstance(self.photo.pk, int)
        self.assertTrue(self.photo.pk)

    def test_photo_has_title(self):
        """Check that photo has its title attribute."""
        self.assertTrue(self.photo.title)

    def test_photo_has_desc(self):
        """Check that photo has its description attribute."""
        self.assertTrue(self.photo.description)

    def test_photo_has_up_date(self):
        """Check that photo uploaded_date is a datetime before now."""
        self.assertGreater(timezone.now(), self.photo.date_uploaded)

    def test_user(self):
        """Test that user attr of Photo is established User."""
        self.assertIs(self.photo.user, self.user)


class MultiPhotoCase(OneUserCase):
    """Test case using many Photo instances."""

    def setUp(self):
        """Add many Photos to the database for testing."""
        super(MultiPhotoCase, self).setUp()

        self.photo_batch = PhotoFactory.create_batch(
            PHOTO_TEST_BATCH_SIZE,
            user=self.user,
            title='Test photo',
            description='Test description',
        )

    def test_correct_batch_size(self):
        """Test that batch of created photos are as many as expected."""
        self.assertEqual(len(self.photo_batch), PHOTO_TEST_BATCH_SIZE)

    def test_user(self):
        """Test that user attr of all Photos is established User."""
        for photo in self.photo_batch:
            self.assertIs(photo.user, self.user)


# class OneAlbumCase()