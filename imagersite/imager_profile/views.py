"""Views for editing the imager profile."""

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserForm, ImagerProfileForm
# from django.contrib.auth.models import User
# from .forms import UserProfileFormSet
# from .models import ImagerProfile


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


# class EditProfileView(UpdateView):
#     """Allow the user to edit their profile."""

#     model = User
#     form_class = UserProfileFormSet
#     template_name = "imager_profile/edit_profile2.html"
#     # fields = ['user__first_name', 'user__last_name', 'camera']
#     success_url = '/profile/'

#     def get_object(self, queryset=None):
#         """Allow only photos of current user as the view queryset."""
#         self.kwargs['pk'] = self.request.user.pk
#         return super(EditProfileView, self).get_object(queryset=queryset)

    # def get_context_data(self, *args, **kwargs):
    #     """Include the formset in the context data."""
    #     data = super(EditProfileView, self).get_context_data(*args, **kwargs)
    #     data['formset'] = UserProfileFormSet(instance=self.request.user)
    #     return data

    # def form_valid(self):
    #     pass
