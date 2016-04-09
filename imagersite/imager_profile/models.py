"""Establish models for the imager site's User Profile."""
from django.db import models as md
from django.contrib.auth.models import User


class ImagerProfile(md.Model):
    """Profile attached to User model by one-to-one relationship."""

    user = md.OneToOneField(User, related_name='profile')
    location = md.CharField(default='', max_length=255)
    camera = md.CharField(default='', max_length=255)
    fav_photo = md.CharField(default='', max_length=255)

    @property
    def is_active(self):
        """Return boolean of associated User's is_active boolean state."""
        return self.user.is_active

    @classmethod
    def active(cls):
        """Return QuerySet of all ImagerProfiles of active users."""
        return cls.objects.filter(is_active=True)
