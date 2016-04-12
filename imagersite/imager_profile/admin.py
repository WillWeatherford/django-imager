"""Register imager_profile models to be available on admin page."""

from django.contrib import admin
from .models import ImagerProfile

admin.site.register(ImagerProfile)
