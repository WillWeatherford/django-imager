"""Views for adding, editing and deleting Photos and Albums."""

from django.views.generic import CreateView, UpdateView, DetailView
from django.db.models import Q
from .models import Photo, Album
from .forms import AlbumForm


class AddOrEditMixin(object):
    """Flexible class view for creation and editing of albums and photos."""

    template_name = 'imager_images/add_or_edit.html'
    success_url = '/images/library/'
    own_queryset_name = None
    rel_queryset_name = None

    def get(self, request, *args, **kwargs):
        """Allow only photos belonging to current user as the view queryset."""
        self.queryset = getattr(self.request.user, self.own_queryset_name)
        return super(AddOrEditMixin, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Provide context data to edit and create pages."""
        context_data = super(
            AddOrEditMixin, self).get_context_data(*args, **kwargs)
        path = self.request.path
        if '/add/' in path:
            context_data['cancel_url'] = self.success_url
            context_data['use_case'] = 'Create'
        else:
            context_data['cancel_url'] = path.replace('edit/', '')
            context_data['use_case'] = 'Edit'
        context_data['model_name'] = self.model.__name__
        return context_data

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super(AddOrEditMixin, self).get_form(form_class=form_class)
        owner_rel_queryset = getattr(self.request.user, self.rel_queryset_name)
        form.fields[self.rel_queryset_name].queryset = owner_rel_queryset
        if self.form_class is AlbumForm:
            form.fields['cover'].queryset = owner_rel_queryset
        return form

    def form_valid(self, form):
        """Insert the user from request context into the form as the owner."""
        form.instance.owner = self.request.user
        return super(AddOrEditMixin, self).form_valid(form)


class CreatePhotoView(AddOrEditMixin, CreateView):
    """Create a new Photo to the database."""

    model = Photo
    fields = ['albums', 'img_file', 'title', 'description', 'published']
    own_queryset_name = 'photos'
    rel_queryset_name = 'albums'


class CreateAlbumView(AddOrEditMixin, CreateView):
    """Create a new Album to the database."""

    model = Album
    form_class = AlbumForm
    own_queryset_name = 'albums'
    rel_queryset_name = 'photos'


class EditPhotoView(AddOrEditMixin, UpdateView):
    """Allows user to edit their own photos."""

    model = Photo
    fields = ['albums', 'title', 'description', 'published']
    own_queryset_name = 'photos'
    rel_queryset_name = 'albums'


class EditAlbumView(AddOrEditMixin, UpdateView):
    """Allows user to edit their own photos."""

    model = Album
    form_class = AlbumForm
    own_queryset_name = 'albums'
    rel_queryset_name = 'photos'


class AlbumPhotoDetailView(DetailView):
    """DetailView subclass to filter only public items to non-owners."""

    def get(self, request, *args, **kwargs):
        """Allow only public queryset or items belonging to current user."""
        query = Q(published='public')
        if request.user.is_authenticated():
            query |= Q(owner=request.user)
        self.queryset = self.model.objects.filter(query).distinct()
        return super(AlbumPhotoDetailView, self).get(request, *args, **kwargs)
