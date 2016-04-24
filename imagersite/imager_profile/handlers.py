# -*- coding: utf-8 -*-
"""Handlers for pop-save and pre-delete events on User model."""
from __future__ import unicode_literals
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from registration.signals import user_activated
from django.dispatch import receiver
from .models import ImagerProfile
from django.contrib.auth.models import Group
import logging

MODELS = ['imagerprofile', 'photo', 'album']
logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_imager_profile(sender, **kwargs):
    """Create and save an ImagerProfile after every new User is created."""
    if kwargs.get('created', False):
        try:
            user = kwargs['instance']
            new_profile = ImagerProfile(user=user)
            new_profile.save()
        except (KeyError, ValueError):
            logger.error('Unable to create ImagerProfile for User instance.')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_permissions(sender, **kwargs):
    """Create and save an ImagerProfile after every new User is created."""
    if kwargs.get('created', False):
        try:
            user = kwargs['instance']
            active_group = Group.objects.get(name='Active Users')
            user.groups.add(active_group)
        except (KeyError, ValueError):
            logger.error('Unable to add Permissions for User instance.')


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def remove_imager_profile(sender, **kwargs):
    """Delete attached ImagerProfile after User is deleted."""
    try:
        instance = kwargs['instance']
        instance.is_active = False
        instance.profile.delete()
    except (KeyError, AttributeError):
        logger.warn('ImagerProfile instance not deleted.')
