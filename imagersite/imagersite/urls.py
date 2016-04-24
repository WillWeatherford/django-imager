"""Imagersite URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView, DetailView, DeleteView
from imager_images.models import Photo, Album
from .views import (
    HomeView,
    CreatePhotoView,
    CreateAlbumView,
    EditAlbumView,
    EditPhotoView,
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
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),

    url(r'^profile/$',
        login_required(TemplateView.as_view(template_name="profile.html")),
        name='profile',),

    url(r'^profile/edit/$',
        log_perm_required(USER, EDIT, edit_profile),
        name='edit_profile'),

    url(r'^images/library/$',
        login_required(TemplateView.as_view(template_name="library.html")),
        name='library'),

    url(r'^images/album/(?P<pk>[0-9]+)/$',
        DetailView.as_view(model=Album, template_name="album.html"),
        name='album_detail'),

    url(r'^images/photo/(?P<pk>[0-9]+)/$',
        DetailView.as_view(model=Photo, template_name="photo.html"),
        name='photo_detail'),

    url(r'^images/album/(?P<pk>[0-9]+)/edit/$',
        log_perm_required(ALBUM, EDIT, EditAlbumView.as_view()),
        name='edit_album'),

    url(r'^images/photo/(?P<pk>[0-9]+)/edit/$',
        log_perm_required(PHOTO, EDIT, EditPhotoView.as_view()),
        name='edit_photo'),

    url(r'^images/photo/add/$',
        log_perm_required(PHOTO, ADD, CreatePhotoView.as_view()),
        name='add_photo'),

    url(r'^images/album/add/$',
        log_perm_required(ALBUM, ADD, CreateAlbumView.as_view()),
        name='add_album'),

    url(r'^images/album/(?P<pk>[0-9]+)/delete/$',
        log_perm_required(
            ALBUM,
            DELETE,
            DeleteView.as_view(
                model=Album,
                template_name='confirm_delete.html',
                success_url='/images/library/',
            )),
        name='delete_album'),

    url(r'^images/photo/(?P<pk>[0-9]+)/delete/$',
        log_perm_required(
            PHOTO,
            DELETE,
            DeleteView.as_view(
                model=Photo,
                template_name='confirm_delete.html',
                success_url='/images/library/',
            )),
        name='delete_photo'),

    # url(r'^profile/edit/$', EditProfileView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
