"""Urls for accessing the Imager data through REST API."""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api import views


urlpatterns = [
    url(r'^photos/$', views.PhotoListView.as_view()),
    # url(r'^api-auth/', include(
    #     'rest_framework.urls',
    #     namespace='rest_framework'))
]
