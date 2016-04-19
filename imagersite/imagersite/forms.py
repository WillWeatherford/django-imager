"""ModelForms to add and edit database objects."""
from django import forms
from imager_images.models import Photo, Album

# ownership filtering
# init method of form
# view's form instance... figuring out which form to use


class AlbumForm(forms.ModelForm):
    """Form for displaying the Photo model."""

    class Meta:
        """Set up the Album and excluded fields for the Album form."""

        model = Album
        exclude = ['date_published', 'owner']

    photos = forms.ModelMultipleChoiceField(
        label='Photos',
        queryset=Photo.objects.all()
    )
