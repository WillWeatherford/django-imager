"""Views at the configuration root level."""

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, UpdateView
from imager_images.models import Photo, Album
from imager_profile.models import ImagerProfile
from .forms import AlbumForm, UserForm, ImagerProfileForm, UserProfileFormSet
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


class CreateOrEditMixin(object):
    """Flexible class view for creation and editing of albums and photos."""

    template_name = 'create_or_edit.html'
    success_url = '/images/library/'
    own_queryset_name = None
    rel_queryset_name = None

    def get(self, request, *args, **kwargs):
        """Allow only photos belonging to current user as the view queryset."""
        self.queryset = getattr(self.request.user, self.own_queryset_name)
        return super(CreateOrEditMixin, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Provide context data to edit and create pages."""
        context_data = super(
            CreateOrEditMixin, self).get_context_data(*args, **kwargs)
        path = self.request.path
        if '/add/' in path:
            context_data['cancel_url'] = self.success_url
            context_data['use_case'] = 'Create'
        else:
            context_data['cancel_url'] = path.replace('edit/', '')
            context_data['use_case'] = 'Edit'
        context_data['model_name'] = self.model.__class__.__name__
        return context_data

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super(CreateOrEditMixin, self).get_form(form_class=form_class)
        owner_rel_queryset = getattr(self.request.user, self.rel_queryset_name)
        form.fields[self.rel_queryset_name].queryset = owner_rel_queryset
        return form

    def form_valid(self, form):
        """Insert the user from request context into the form as the owner."""
        form.instance.owner = self.request.user
        return super(CreateOrEditMixin, self).form_valid(form)


class CreatePhotoView(CreateOrEditMixin, CreateView):
    """Create a new Photo to the database."""

    model = Photo
    fields = ['albums', 'img_file', 'title', 'description', 'published']
    own_queryset_name = 'photos'
    rel_queryset_name = 'albums'


class CreateAlbumView(CreateOrEditMixin, CreateView):
    """Create a new Album to the database."""

    model = Album
    form_class = AlbumForm
    own_queryset_name = 'albums'
    rel_queryset_name = 'photos'


class EditPhotoView(CreateOrEditMixin, UpdateView):
    """Allows user to edit their own photos."""

    model = Photo
    fields = ['albums', 'title', 'description', 'published']
    own_queryset_name = 'photos'
    rel_queryset_name = 'albums'


class EditAlbumView(CreateOrEditMixin, UpdateView):
    """Allows user to edit their own photos."""

    model = Album
    form_class = AlbumForm
    own_queryset_name = 'albums'
    rel_queryset_name = 'photos'


def edit_profile(request):
    """Allow user to edit their ImagerProfile, and limited fields of User."""
    user = request.user
    profile = request.user.profile
    user_form = UserForm(instance=user)
    profile_form = ImagerProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ImagerProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/profile/')
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'edit_profile.html', context)


class EditProfileView(UpdateView):
    """Allow the user to edit their profile."""

    model = User
    form_class = UserProfileFormSet
    template_name = "edit_profile2.html"
    # fields = ['user__first_name', 'user__last_name', 'camera']
    success_url = '/profile/'

    def get_object(self, queryset=None):
        """Allow only photos belonging to current user as the view queryset."""
        self.kwargs['pk'] = self.request.user.pk
        return super(EditProfileView, self).get_object(queryset=queryset)

    # def get_context_data(self, *args, **kwargs):
    #     """Include the formset in the context data."""
    #     data = super(EditProfileView, self).get_context_data(*args, **kwargs)
    #     data['formset'] = UserProfileFormSet(instance=self.request.user)
    #     return data

    # def form_valid(self):
    #     pass
