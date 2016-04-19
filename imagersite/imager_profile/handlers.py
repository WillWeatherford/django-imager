# -*- coding: utf-8 -*-
"""Handlers for pop-save and pre-delete events on User model."""
from __future__ import unicode_literals
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import ImagerProfile
from django.contrib.auth.models import Permission
import logging

MODELS = ['imagerprofile', 'photo', 'album']
# PERMS = ['add', 'change', 'delete']
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
            perm = Permission.objects.get(codename='add_photo')
            user.user_permission.add(perm)
            # user.save()
            # for model in MODELS:
            #     perm_set = Permission.objects.filter(codename__contains=model)
            #     user.user_permissions.set(perm_set)
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
