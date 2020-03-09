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
    class Meta:
        model = Author
        fields = ['email', 'firstName', 'lastName', 'password1', 'password2']
        exclude = ['profile_img']
        # exclude = ('bio', 'github', 'displayName',)
