"""Establish Python representations of Photos and Albums database tables."""
from django.db import models as md
from django.conf import settings

PUB_CHOICES = ['private', 'shared', 'public']
PUB_DEFAULT = PUB_CHOICES[0]
PUB_FIELD_CHOICES = zip(PUB_CHOICES, PUB_CHOICES)
DATE_FORMAT = '%d %B %Y %I:%M%p'


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

    def __str__(self):
        """String output of Photo instance."""
        return "{}... ({})".format(
            self.title[:20],
            self.date_published.strftime(DATE_FORMAT))

    def __repr__(self):
        """Command line representation of Photo instance."""
        return "Photo(title={}, owner={}, date_published={}".format(
            self.title[:20],
            self.owner,
            self.date_published.strftime(DATE_FORMAT))


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
        if photo.owner != self.owner:
            raise ValueError('{} is not owned by {}.'.format(
                photo, self.owner))
        if photo not in self.photos.all():
            raise KeyError('{} is not in {}, so it cannot be the cover photo.'
                           ''.format(photo, self.title))
        self.cover = photo
        self.save()

    def _owned_photos(self, photos):
        """Generate only photos owned by the owner of the album."""
        for photo in photos:
            if photo.owner == self.owner:
                yield photo

    def add_photos(self, photos):
        """Set this album on the relationship to all photos in iterable."""
        for photo in self._owned_photos(photos):
            photo.albums.add(self)
            photo.save()
            if self.cover is None:
                self.set_cover(photo)
