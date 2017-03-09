from django.contrib.auth.models import User
from django import forms
from registration.forms import RegistrationForm


class UserFormUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserProfileForm(RegistrationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserProfileFormUpdate(RegistrationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']