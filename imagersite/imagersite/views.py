"""Views at the configuration root level."""

from django.views.generic import TemplateView, CreateView
from imager_images.models import Photo
# from .forms import PhotoForm
DEFAULT_IMG_URL = 'media/django-magic.jpg'


class HomeView(TemplateView):
    """Generic home view showing public image to any user."""

    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        """Return dictionary of context information for home view."""
        img_url = DEFAULT_IMG_URL
        user_photo = Photo.public.random()
        if user_photo:
            img_url = user_photo.img_file.url

        return {'img_url': img_url}


class CreatePhotoView(CreateView):
    """Create."""

    # form_class = PhotoForm
    model = Photo
    template_name = 'create_photo.html'
    success_url = '/images/library/'
    fields = [
        'albums',
        'img_file',
        'title',
        'description',
        'published',
    ]

    def form_valid(self, form):
        """Insert the user from request context into the form as the owner."""
        form.instance.owner = self.request.user
        return super(CreatePhotoView, self).form_valid(form)
