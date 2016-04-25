"""Views at the configuration root level."""

from django.views.generic import TemplateView
from imager_images.models import Photo

DEFAULT_IMG_URL = 'media/django-magic.jpg'


class HomeView(TemplateView):
    """Generic home view showing public image to any user."""

    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        """Return dictionary of context information for home view."""
        context_data = super(HomeView, self).get_context_data(*args, **kwargs)
        try:
            user_photo = Photo.public.random()
            context_data['img_url'] = user_photo.img_file.url
        except AttributeError:
            context_data['img_url'] = DEFAULT_IMG_URL
        return context_data
