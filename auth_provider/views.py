from typing import Any, Dict
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, logout
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from auth_provider.user_resources import user_resources
from .forms import SignUpForm, EditProfileForm


class SignUpView(CreateView):
    template_name = 'auth/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('auth_provider:login')


class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'profile/user_profile.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_resources'] = [{'name': user_resource[0], 'link': user_resource[1]}
                                     for user_resource in user_resources]
        return context


class EditProfileView(UpdateView):
    form_class = EditProfileForm
    model = get_user_model()
    template_name = 'profile/edit_profile.html'

    def get_object(self):
        return self.request.user


def logout_view(request):
    logout(request)
    return redirect('/')
