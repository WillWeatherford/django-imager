"""Establish Python representations of Photos and Albums database tables."""
from django.db import models as md

PUB_CHOICES = ['private', 'shared', 'public']
PUB_DEFAULT = PUB_CHOICES[0]
PUB_FIELD_CHOICES = zip(PUB_CHOICES, PUB_CHOICES)


class Photo(md.Model):
    """Base class representing a single image in the database."""

    # user
    title = md.CharField(max_length=255)
    description = md.TextField()
    date_uploaded = md.DateTimeField(auto_now_add=True)
    date_modified = md.DateTimeField(auto_now=True)
    date_published = md.DateTimeField()
    published = md.CharField(max_length=255,
                             choices=PUB_FIELD_CHOICES,
                             default=PUB_DEFAULT)
