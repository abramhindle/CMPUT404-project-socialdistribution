from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


# class RegistrationForm(UserCreationForm):
class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['username', 'password']


class LoginForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['username', 'password']
