from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import Author
from django.contrib.auth.models import User

class ProfileForm(UserCreationForm):

    class Meta:
        model = Author
        fields = [
            'firstName',
            'lastName',
            'displayName',
            'bio',
            'github',
            'profile_img',
        ]

class ProfileSignup(UserCreationForm):
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=("Enter the same password as above, for verification."))
    class Meta:
        model = Author
        fields = ['firstName', 'lastName', 'email', 'password1', 'password2']
