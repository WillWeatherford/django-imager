"""Urls for accessing the Imager data through REST API."""
from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^photos/$', views.PhotoListView.as_view(), name='photos'),
    url(r'^albums/$', views.AlbumListView.as_view(), name='albums'),
    # url(r'^albums/(?P<pk>[0-9]+)/$',
    #     views.AlbumPhotoListView.as_view(),
    #     'album-photo-list'),
]
