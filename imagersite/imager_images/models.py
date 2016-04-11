"""Establish Python representations of Photos and Albums database tables."""
from django.db import models as md
from django.conf import settings

PUB_CHOICES = ['private', 'shared', 'public']
PUB_DEFAULT = PUB_CHOICES[0]
PUB_FIELD_CHOICES = zip(PUB_CHOICES, PUB_CHOICES)


class Photo(md.Model):
    """Represents a single image in the database."""

    owner = md.ForeignKey(settings.AUTH_USER_MODEL,
                          related_name='photos',
                          default=None)
    # albums = md.ManyToManyField(Album, related_name='photos')
    title = md.CharField(max_length=255)
    description = md.TextField()
    date_uploaded = md.DateTimeField(auto_now_add=True)
    date_modified = md.DateTimeField(auto_now=True)
    date_published = md.DateTimeField(auto_now_add=True)
    published = md.CharField(max_length=255,
                             choices=PUB_FIELD_CHOICES,
                             default=PUB_DEFAULT)


class Album(md.Model):
    """Represents a collection of images in the database."""

    owner = md.ForeignKey(settings.AUTH_USER_MODEL,
                          related_name='albums')
    # photos = md.ManyToManyField(Photo, related_name='albums')
    title = md.CharField(max_length=255)
    description = md.TextField()
    date_created = md.DateTimeField(auto_now_add=True)
    date_modified = md.DateTimeField(auto_now=True)
    date_published = md.DateTimeField(auto_now_add=True)
    published = md.CharField(max_length=255,
                             choices=PUB_FIELD_CHOICES,
                             default=PUB_DEFAULT)
    # cover

    def set_cover(self):
        pass

    def add_photo(self):
        pass

    def remove_photo(self):
        pass

# The albums created by a user may contain only Photos created by that same user.
