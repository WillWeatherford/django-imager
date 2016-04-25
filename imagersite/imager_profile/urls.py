"""Establish url patterns for the user profile views."""
from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView, DetailView, DeleteView

from .views import (
    # EditProfileView,
    edit_profile,
)


ADD, EDIT, DELETE = 'add', 'change', 'delete'
USER = 'auth.{}_user'
PROFILE = 'imager_profile.{}_imagerprofile'
ALBUM = 'imager_images.{}_album'
PHOTO = 'imager_images.{}_photo'


def log_perm_required(model, perm, view):
    """Shortcut to wrap a view in both login_ and permission_required."""
    perm_name = model.format(perm)
    return login_required(
        permission_required(
            perm_name, raise_exception=True)(view))


urlpatterns = [
    url(r'^$',
        login_required(TemplateView.as_view(template_name="profile.html")),
        name='profile',),

    url(r'^edit/$',
        log_perm_required(USER, EDIT, edit_profile),
        name='edit_profile'),
]
