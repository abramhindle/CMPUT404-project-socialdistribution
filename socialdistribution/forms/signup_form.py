from django import forms
from django.views.generic.edit import FormView
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def create_user(self):
        data = self.cleaned_data
        User.objects.create_user(username=data['username'], password=data['password'])


class SignUpView(FormView):
    template_name = 'auth/signup.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form: SignUpForm):
        form.create_user()
        return super().form_valid(form)
