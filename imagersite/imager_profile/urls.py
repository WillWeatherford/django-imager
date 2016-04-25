"""Establish url patterns for the user profile views."""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

from .views import (
    # EditProfileView,
    edit_profile,
)


HERE = 'imager_profile'
ADD, EDIT, DELETE = 'add', 'change', 'delete'
USER = 'auth.{}_user'
PROFILE = HERE + '.{}_imagerprofile'


def log_perm_required(model, perm, view):
    """Shortcut to wrap a view in both login_ and permission_required."""
    perm_name = model.format(perm)
    return login_required(
        permission_required(
            perm_name, raise_exception=True)(view))


urlpatterns = [
    url(r'^$',
        login_required(
            TemplateView.as_view(template_name=HERE + '/profile.html')),
        name='profile',),

    url(r'^edit/$',
        log_perm_required(USER, EDIT, edit_profile),
        name='edit_profile'),
]
