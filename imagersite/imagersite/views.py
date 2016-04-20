"""Views at the configuration root level."""

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, UpdateView
from imager_images.models import Photo, Album
from .forms import AlbumForm, UserForm, ImagerProfileForm
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

    model = Album
    form_class = AlbumForm
    template_name = 'create_obj.html'
    success_url = '/images/library/'
    fields = [
        'cover',
        'title',
        'description',
        'published',
    ]

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
    fields = [
        'cover',
        'title',
        'description',
        'published',
    ]

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


def edit_profile(request):
    user = request.user
    profile = request.user.profile
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ImagerProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/profile/')
    user_form = UserForm(instance=user)
    profile_form = ImagerProfileForm(instance=profile)
    import pdb;pdb.set_trace()
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'edit_profile.html', context)


# class EditProfileView(TemplateView):
#     """Allow the user to edit their profile."""

#     template_name = "edit_profile.html"
#     # fields = ['friends', 'location', 'camera', 'fav_photo'],
#     success_url = '/profile/'

#     def get_context_data(self, *args, **kwargs):
#         """Include the formset in the context data."""
#         data = super(EditProfileView, self).get_context_data(*args, **kwargs)
#         data['formset'] = UserProfileFormSet(instance=self.request.user)
#         return data


    # def form_valid(self):
    #     pass

