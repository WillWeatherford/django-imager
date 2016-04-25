"""Establish url patterns for the user profile views."""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from url_utils import log_perm_required, EDIT

from .views import (
    edit_profile,
    # EditProfileView,
)


HERE = 'imager_profile'
USER = 'auth.{}_user'
PROFILE = HERE + '.{}_imagerprofile'


urlpatterns = [
    url(r'^$',
        login_required(
            TemplateView.as_view(template_name=HERE + '/profile.html')),
        name='profile',),

    url(r'^edit/$',
        log_perm_required(USER, EDIT, edit_profile),
        name='edit_profile'),
]
