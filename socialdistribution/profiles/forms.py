from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author


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
