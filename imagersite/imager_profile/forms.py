"""Forms for editing the imager profile."""

from django import forms
from imager_profile.models import ImagerProfile
from django.contrib.auth.models import User
# from django.forms import inlineformset_factory


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


# UserProfileFormSet = inlineformset_factory(
#     User,
#     ImagerProfile,
#     fields=('camera', 'location')
# )
