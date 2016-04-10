"""Test that Photo and Album models work as expected."""
from __future__ import unicode_literals
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from .models import Photo
import factory

PHOTO_TEST_BATCH_SIZE = 20


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for User model in tests."""

    class Meta:
        """Establish User model as the product of this factory."""

        model = settings.AUTH_USER_MODEL


class PhotoFactory(factory.django.DjangoModelFactory):
    """Creates Photo models for testing."""

    class Meta:
        """Assign Photo model as product of factory."""

        model = Photo


class BasicPhotoCase(TestCase):
    """Simple test case for Photos."""

    def setUp(self):
        """Add one Photo to the database for testing."""
        # self.user = UserFactory.create(
        #     username='testuser',
        #     email='testuser@example.com',
        # )
        # self.user.set_password('secret')

        self.photo = PhotoFactory.create(
            # user=self.user,
            title='Test photo',
            description='Test description',
        )

    def test_photo_exists(self):
        """Test that the photo set up from the factory does exist."""
        self.assertTrue(self.photo)

    def test_photo_has_title(self):
        """Check that photo has its title attribute."""
        self.assertTrue(self.photo.title)

    def test_photo_has_desc(self):
        """Check that photo has its description attribute."""
        self.assertTrue(self.photo.description)

    def test_photo_has_up_date(self):
        """Check that photo uploaded_date is a datetime before now."""
        self.assertGreater(timezone.now(), self.photo.date_uploaded)


class MultiPhotoCase(TestCase):
    """Test case using many Photo instances."""

    def setUp(self):
        """Add many Photos to the database for testing."""
        self.photo_batch = PhotoFactory.create_batch(
            PHOTO_TEST_BATCH_SIZE,
            title='Test photo',
            description='Test description',
        )

    def test_correct_batch_size(self):
        self.assertEqual(len(self.photo_batch), PHOTO_TEST_BATCH_SIZE)
