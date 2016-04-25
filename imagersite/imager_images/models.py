"""Establish Python representations of Photos and Albums database tables."""
from django.db import models as md
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

PUB_CHOICES = ['private', 'shared', 'public']
PUB_DEFAULT = PUB_CHOICES[0]
PHOTO_PUB_CHOICES = zip(PUB_CHOICES, PUB_CHOICES)
ALBUM_PUB_CHOICES = zip(PUB_CHOICES, PUB_CHOICES)
DATE_FORMAT = '%d %B %Y %I:%M%p'


class PublicManager(md.Manager):
    """QuerySet of Photos which are published."""

    def get_queryset(self):
        """Return QuerySet filtering only Photos which are public."""
        queryset = super(PublicManager, self).get_queryset()
        return queryset.filter(published='public')

    def random(self):
        """Return a single random public photo."""
        queryset = self.get_queryset()
        return queryset.order_by('?').first()


@python_2_unicode_compatible
class Photo(md.Model):
    """Represents a single image in the database."""

    owner = md.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=md.CASCADE,
        related_name='photos')
    albums = md.ManyToManyField('Album', related_name='photos', blank=True)
    img_file = md.ImageField(upload_to='img_files')
    title = md.CharField(max_length=255)
    description = md.TextField()
    date_uploaded = md.DateTimeField(auto_now_add=True)
    date_modified = md.DateTimeField(auto_now=True)
    date_published = md.DateTimeField(null=True)
    published = md.CharField(max_length=255,
                             choices=PHOTO_PUB_CHOICES,
                             default=PUB_DEFAULT)
    objects = md.Manager()
    public = PublicManager()

    def __str__(self):
        """String output of Photo instance."""
        return "{}... ({})".format(self.title[:20], _pub_date(self))

    def __repr__(self):
        """Command line representation of Photo instance."""
        name = '.'.join((__name__, self.__class__.__name__))
        return "{}(title={}, owner={}, date_published={}".format(
            name, self.title[:20], self.owner, _pub_date(self))


@python_2_unicode_compatible
class Album(md.Model):
    """Represents a collection of images in the database."""

    owner = md.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=md.CASCADE,
        related_name='albums',
    )
    cover = md.ForeignKey(
        'Photo', on_delete=md.CASCADE,
        related_name='covered_albums',
        null=True,
        blank=True,
        default=None,
    )
    title = md.CharField(max_length=255)
    description = md.TextField()
    date_created = md.DateTimeField(auto_now_add=True)
    date_modified = md.DateTimeField(auto_now=True)
    date_published = md.DateTimeField(null=True)
    published = md.CharField(
        max_length=255,
        choices=ALBUM_PUB_CHOICES,
        default=PUB_DEFAULT
    )

    def __str__(self):
        """String output of Album instance."""
        return "{}... ({})".format(self.title[:20], _pub_date(self))

    def __repr__(self):
        """Command line representation of Album instance."""
        name = '.'.join((__name__, self.__class__.__name__))
        return "{}(title={}, owner={}, date_published={})".format(
            name, self.title[:20], self.owner, _pub_date(self))

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

    def get_cover(self):
        """Return the user set cover of album or a default image."""
        if self.cover:
            return self.cover.img_file
        item = Photo.objects.get(img_file='DEFAULT_IMAGE')
        return item.img_file


def _pub_date(obj):
    """Return formatted datetime from given object or unpublished."""
    try:
        return obj.date_published.strftime(DATE_FORMAT)
    except AttributeError:
        return 'Unpublished'
