# -*- coding: utf-8 -*-
"""Handlers for pop-save and pre-delete events on User model."""
from __future__ import unicode_literals
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import ImagerProfile
import logging


logger = logging.getLogger(__name__)


# Will this create a new ImagerProfile after user has been edited?
# Or is User only ever saved once, when first created?
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_imager_profile(sender, **kwargs):
    """Create and save an ImagerProfile after every new User is created."""
    if kwargs.get('created', False):
        try:
            new_profile = ImagerProfile(user=kwargs['instance'])
            new_profile.save()
        except (KeyError, ValueError):
            logger.error('Unable to create ImagerProfile for User instance.')


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def remove_imager_profile(sender, **kwargs):
    """Delete attached ImagerProfile after User is deleted."""
    try:
        instance = kwargs['instance']
        instance.is_active = False
        instance.profile.delete()
    except (KeyError, AttributeError):
        logger.warn('ImagerProfile instance not deleted.')
