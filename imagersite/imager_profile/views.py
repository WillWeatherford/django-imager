"""Views for editing the imager profile."""

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserForm, ImagerProfileForm


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
    return render(request, 'imager_profile/edit_profile.html', context)
