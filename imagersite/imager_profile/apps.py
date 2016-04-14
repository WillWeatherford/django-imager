"""Initialize imager_profile apps."""
from django.apps import AppConfig


class ImagerProfileConfig(AppConfig):
    """Set up Config for the imager_profile app."""

    name = 'imager_profile'

    def ready(self):
        """Run code when the app is ready."""
        from imager_profile import handlers
