# -*- coding: utf-8 -*-
"""Handlers for pop-save and pre-delete events on User model."""
from __future__ import unicode_literals
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from registration.signals import user_activated
from registration.backends.hmac.views import ActivationView
from django.dispatch import receiver
from .models import ImagerProfile
from django.contrib.auth.models import Permission
import logging

logger = logging.getLogger(__name__)

MODELS = ['photo', 'album']
ACTIONS = ['add', 'change', 'delete']
PERMS = ['_'.join((action, model)) for action in ACTIONS for model in MODELS]
PERMS += ['change_user', 'change_imagerprofile']


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


@receiver(user_activated, sender=ActivationView)
def add_permissions(sender, **kwargs):
    """Create and save an ImagerProfile after every new User is created."""
    try:
        user = kwargs['user']
        try:
            for codename in PERMS:
                perm = Permission.objects.get(codename=codename)
                user.user_permissions.add(perm)
        except Permission.DoesNotExist:
            logger.error('Permission not found.')
    except (KeyError, ValueError):
        logger.error('User not sent with user_activated signal.')


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def remove_imager_profile(sender, **kwargs):
    """Delete attached ImagerProfile after User is deleted."""
    try:
        instance = kwargs['instance']
        instance.is_active = False
        instance.profile.delete()
        instance.save()
    except (KeyError, AttributeError):
        logger.warn('ImagerProfile instance not deleted.')
