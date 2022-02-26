from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm


class SignUpView(CreateView):
    template_name = 'auth/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('auth_provider:login')
