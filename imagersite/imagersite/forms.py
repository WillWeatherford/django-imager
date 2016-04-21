"""ModelForms to add and edit database objects."""
from django import forms
from django.forms import inlineformset_factory
from imager_images.models import Photo, Album
from imager_profile.models import ImagerProfile
from django.contrib.auth.models import User


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


class UserForm(forms.ModelForm):
    """Modifying limited fields on the User model."""

    class Meta:
        """Establish Model and fields for user form."""

        model = User
        fields = ['first_name', 'last_name', 'email']


class ImagerProfileForm(forms.ModelForm):
    """Editable Profile for the user."""

    class Meta:
        """Establish Model and fields for user form."""

        model = ImagerProfile
        exclude = ['user', 'friends']


UserProfileFormSet = inlineformset_factory(
    User,
    ImagerProfile,
    fields=('camera', 'location')
)
