from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    """
        Create User Form Configuration
    """
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']