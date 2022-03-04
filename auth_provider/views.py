from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from .forms import SignUpForm


class SignUpView(CreateView):
    template_name = 'auth/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('auth_provider:login')


class ProfileView(DetailView):
    model = get_user_model
    template_name = 'profile/user_profile.html'

    def get_object(self):
        return self.request.user
