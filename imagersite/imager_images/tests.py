from __future__ import unicode_literals
from django.test import TestCase
from models import Photo
import datetime
import factory


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo


class BasicPhotoCase(TestCase):
    """Simple test case for Photos."""

    def setUp(self):
        self.photo = PhotoFactory.create(
            title='Test photo',
            description='Test description',
        )

    def test_photo_exists(self):
        self.assertIsNotNone(self.photo)

    def test_photo_has_title(self):
        self.assertIsNotNone(self.photo.title)

    def test_photo_has_desc(self):
        self.assertIsNotNone(self.photo.description)

    def test_photo_has_up_date(self):
        self.assertGreater(datetime.now(), self.photo.date_uploaded)
