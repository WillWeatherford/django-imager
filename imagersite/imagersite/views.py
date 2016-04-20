"""Views at the configuration root level."""

from django.views.generic import TemplateView, CreateView, UpdateView
from imager_images.models import Photo, Album
from .forms import AlbumForm
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
    """Create a new Photo to the database."""

    model = Photo
    template_name = 'create_obj.html'
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

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super(CreatePhotoView, self).get_form(form_class=form_class)
        form.fields['albums'].queryset = self.request.user.albums
        return form


class CreateAlbumView(CreateView):
    """Create a new Album to the database."""

    form_class = AlbumForm
    template_name = 'create_obj.html'
    success_url = '/images/library/'

    def form_valid(self, form):
        """Insert the user from request context into the form as the owner."""
        form.instance.owner = self.request.user
        return super(CreateAlbumView, self).form_valid(form)

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super(CreateAlbumView, self).get_form(form_class=form_class)
        form.fields['photos'].queryset = self.request.user.photos
        return form


class EditAlbumView(UpdateView):
    """Allows user to edit their own photos."""

    model = Album
    form_class = AlbumForm
    template_name = "edit_obj.html"
    success_url = '/images/library/'

    def get(self, request, *args, **kwargs):
        """Allow only albums belonging to current user as the view queryset."""
        self.queryset = request.user.albums
        return super(EditAlbumView, self).get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super(EditAlbumView, self).get_form(form_class=form_class)
        form.fields['photos'].queryset = self.request.user.photos
        return form


class EditPhotoView(UpdateView):
    """Allows user to edit their own photos."""

    model = Photo
    template_name = "edit_obj.html"
    success_url = '/images/library/'
    fields = ['albums', 'title', 'description', 'published']

    def get(self, request, *args, **kwargs):
        """Allow only photos belonging to current user as the view queryset."""
        self.queryset = request.user.photos
        return super(EditPhotoView, self).get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super(EditPhotoView, self).get_form(form_class=form_class)
        form.fields['albums'].queryset = self.request.user.albums
        return form

# class EditProfileView(UpdateView):
#     """Allow the user to edit their profile."""

#     model = ImagerProfile,
#     template_name = "edit_obj.html",
#     fields = ['friends', 'location', 'camera', 'fav_photo'],
#     success_url = '/profile/'
