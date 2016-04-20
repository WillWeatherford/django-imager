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
from django.views.generic import TemplateView, DetailView, UpdateView
from imager_images.models import Photo, Album
from imager_profile.models import ImagerProfile
from .views import (
    HomeView,
    CreatePhotoView,
    CreateAlbumView,
    EditAlbumView,
    EditPhotoView
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home_page'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),

    url(r'^profile/$', login_required(
        TemplateView.as_view(template_name="profile.html"))),
    url(r'^images/library/$', login_required(
        TemplateView.as_view(template_name="library.html"))),

    url(r'^images/album/(?P<pk>[0-9]+)/$',
        DetailView.as_view(model=Album, template_name="album.html")),
    url(r'^images/photo/(?P<pk>[0-9]+)/$',
        DetailView.as_view(model=Photo, template_name="photo.html")),

    url(r'^images/album/(?P<pk>[0-9]+)/edit/$',
        login_required(
            permission_required(
                'imager_images.change_album',
                raise_exception=True,
            )(EditAlbumView.as_view())
        )),

    url(r'^images/photo/(?P<pk>[0-9]+)/edit/$',
        login_required(
            permission_required(
                'imager_images.change_photo',
                raise_exception=True,
            )(EditPhotoView.as_view()))),
    url(r'^images/photo/add/$',
        login_required(
            permission_required(
                'imager_images.change_photo',
                raise_exception=True,
            )(CreatePhotoView.as_view())
        )),
    url(r'^images/album/add/$',
        login_required(
            permission_required(
                'imager_images.change_photo',
                raise_exception=True,
            )(CreateAlbumView.as_view())
        )),
    # url(r'^profile/edit/$',
    #     UpdateView.as_view()),
]

# (?P<pk>[0-9]+)/$

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
