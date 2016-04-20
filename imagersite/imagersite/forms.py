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


class UserForm(forms.ModelForm):
    """Modifying limited fields on the User model."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ImagerProfileForm(forms.ModelForm):
    """Editable Profile for the user."""

    class Meta:
        model = ImagerProfile
        exclude = ['user', 'friends']
