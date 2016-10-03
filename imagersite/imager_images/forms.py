"""Forms for adding, editing and deleting Albums and Photos."""

from django import forms
from .models import Photo, Album


class AlbumForm(forms.ModelForm):
    """Form for displaying the Photo model."""

    class Meta:
        """Set up the Album and excluded fields for the Album form."""

        model = Album
        exclude = ['date_published', 'owner']

    photos = forms.ModelMultipleChoiceField(
        label='Photos',
        required=False,
        queryset=Photo.objects.all()
    )

    def save(self, commit=True):
        """Extend ModelForm save method ensuring we add photos to album."""
        photos = self.cleaned_data['photos']
        instance = super(AlbumForm, self).save(commit)
        instance.photos.add(*photos)
        return instance
