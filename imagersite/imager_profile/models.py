"""Establish models for the imager site's User Profile."""
from django.db import models
from django.contrib.auth.models import User


class ImagerProfile(models.Model):
    """Profile attached to User models by one-to-one relationship."""

    user = models.OneToOneField(User, related_name='profile')
    is_active = models.BooleanField(default=False)
    location = models.CharField(default='')
    camera = models.CharField(default='')
    fav_photo = models.CharField(default='')
