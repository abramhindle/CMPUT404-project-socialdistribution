from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

# https://stackoverflow.com/questions/13202845/removing-help-text-from-django-usercreateform

# class RegistrationForm(UserCreationForm):


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'bio', 'github']
        widgets = {
            'password': forms.PasswordInput(),
        }


class LoginForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['username', 'password']


class NewPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'link_to_image', 'author', 'contentType', 'categories','visibility', 'unlisted']
        widgets = {
            'contentType': forms.Select(),
            'link_to_image': forms.URLInput(),
            'visibility': forms.Select(),
            'author': forms.HiddenInput()
        }
