"""Establish Python representations of Photos and Albums database tables."""
from django.db import models as md
from django.conf import settings

PUB_CHOICES = ['private', 'shared', 'public']
PUB_DEFAULT = PUB_CHOICES[0]
PUB_FIELD_CHOICES = zip(PUB_CHOICES, PUB_CHOICES)


class Photo(md.Model):
    """Represents a single image in the database."""

    owner = md.ForeignKey(settings.AUTH_USER_MODEL,
                          related_name='photos')
    albums = md.ManyToManyField('Album', related_name='photos')
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
    cover = md.ForeignKey('Photo',
                          related_name='covered_albums',
                          null=True,
                          default=None)
    title = md.CharField(max_length=255)
    description = md.TextField()
    date_created = md.DateTimeField(auto_now_add=True)
    date_modified = md.DateTimeField(auto_now=True)
    date_published = md.DateTimeField(auto_now_add=True)
    published = md.CharField(max_length=255,
                             choices=PUB_FIELD_CHOICES,
                             default=PUB_DEFAULT)

    def set_cover(self, photo):
        """Set provided photo as the cover for this album."""
        self.cover = photo
        self.save()

    def add_photos(self, photos):
        """Set this album on the relationship to all photos in iterable."""
        for photo in photos:
            if photo.owner is self.owner:
                photo.albums.add(self)
                photo.save()
                if self.cover is None:
                    self.set_cover(photo)

    def remove_photo(self):
        pass

# The albums created by a user may contain only Photos created by that same user.
