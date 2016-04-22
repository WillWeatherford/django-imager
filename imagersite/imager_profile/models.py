"""Establish models for the imager site's User Profile."""
from django.db import models as md
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


class ActiveManager(md.Manager):
    """QuerySet of ImagerProfiles attached to an active User."""

    def get_queryset(self):
        """Return QuerySet filtering only ImagerProfiles with active users."""
        queryset = super(ActiveManager, self).get_queryset()
        return queryset.filter(user__is_active=True)


@python_2_unicode_compatible
class ImagerProfile(md.Model):
    """Profile attached to User model by one-to-one relationship."""

    user = md.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    friends = md.ManyToManyField('self', related_name='friends')
    location = md.CharField(null=True, blank=True, max_length=255)
    camera = md.CharField(null=True, blank=True, max_length=255)
    fav_photo = md.CharField(null=True, blank=True, max_length=255)

    objects = md.Manager()
    active = ActiveManager()

    def __str__(self):
        """String output of ImagerProfile model."""
        return "Imager profile for {}".format(self.user)

    def __repr__(self):
        """Command line interface representation of ImagerProfile model."""
        name = '.'.join((__name__, self.__class__.__name__))
        return "{}(user={})".format(name, self.user)

    @property
    def is_active(self):
        """Return boolean of associated User's is_active boolean state."""
        return self.user.is_active

    def add_friend(self, other_user):
        """Take a User make a new relationship with its profile."""
        self.friends.add(other_user.profile)
