"""Register imager_images models to be available on admin page."""

from django.contrib import admin
from .models import Photo, Album

admin.site.register(Photo)
admin.site.register(Album)
