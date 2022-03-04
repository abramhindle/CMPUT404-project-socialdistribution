from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
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


class EditProfileView(UpdateView):
    form_class = EditProfileForm
    model = get_user_model()
    template_name = 'profile/edit_profile.html'

    def get_object(self):
        return self.request.user
