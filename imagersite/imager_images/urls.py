"""Establish url patterns for the photo and album views."""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, DeleteView
from imager_images.models import Photo, Album
from url_utils import log_perm_required, ADD, EDIT, DELETE
from .views import (
    CreatePhotoView,
    CreateAlbumView,
    EditAlbumView,
    EditPhotoView,
    AlbumPhotoDetailView,
)
HERE = 'imager_images'
ALBUM = HERE + '.{}_album'
PHOTO = HERE + '.{}_photo'


urlpatterns = [
    url(r'^library/$',
        login_required(
            TemplateView.as_view(template_name=HERE + '/library.html')),
        name='library'),

    url(r'^album/(?P<pk>[0-9]+)/$',
        AlbumPhotoDetailView.as_view(
            model=Album,
            template_name=HERE + '/album.html'),
        name='album_detail'),

    url(r'^photo/(?P<pk>[0-9]+)/$',
        AlbumPhotoDetailView.as_view(
            model=Photo,
            template_name=HERE + '/photo.html'),
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
