"""Establish url patterns for the photo and album views."""

from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url
from django.views.generic import TemplateView, DetailView, DeleteView
from imager_images.models import Photo, Album
from .views import (
    CreatePhotoView,
    CreateAlbumView,
    EditAlbumView,
    EditPhotoView,
)
HERE = 'imager_images'
ADD, EDIT, DELETE = 'add', 'change', 'delete'
ALBUM = HERE + '.{}_album'
PHOTO = HERE + '.{}_photo'


def log_perm_required(model, perm, view):
    """Shortcut to wrap a view in both login_ and permission_required."""
    perm_name = model.format(perm)
    return login_required(
        permission_required(
            perm_name, raise_exception=True)(view))


urlpatterns = [
    url(r'^library/$',
        login_required(
            TemplateView.as_view(template_name=HERE + '/library.html')),
        name='library'),

    url(r'^album/(?P<pk>[0-9]+)/$',
        DetailView.as_view(model=Album, template_name=HERE + '/album.html'),
        name='album_detail'),

    url(r'^photo/(?P<pk>[0-9]+)/$',
        DetailView.as_view(model=Photo, template_name=HERE + '/photo.html'),
        name='photo_detail'),

    url(r'^album/(?P<pk>[0-9]+)/edit/$',
        log_perm_required(ALBUM, EDIT, EditAlbumView.as_view()),
        name='edit_album'),

    url(r'^photo/(?P<pk>[0-9]+)/edit/$',
        log_perm_required(PHOTO, EDIT, EditPhotoView.as_view()),
        name='edit_photo'),

    url(r'^photo/add/$',
        log_perm_required(PHOTO, ADD, CreatePhotoView.as_view()),
        name='add_photo'),

    url(r'^album/add/$',
        log_perm_required(ALBUM, ADD, CreateAlbumView.as_view()),
        name='add_album'),

    url(r'^album/(?P<pk>[0-9]+)/delete/$',
        log_perm_required(
            ALBUM,
            DELETE,
            DeleteView.as_view(
                model=Album,
                template_name=HERE + '/confirm_delete.html',
                success_url='/images/library/',
            )),
        name='delete_album'),

    url(r'^photo/(?P<pk>[0-9]+)/delete/$',
        log_perm_required(
            PHOTO,
            DELETE,
            DeleteView.as_view(
                model=Photo,
                template_name=HERE + '/confirm_delete.html',
                success_url='/images/library/',
            )),
        name='delete_photo'),
]
