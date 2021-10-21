from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    display_name = forms.CharField(max_length=30, required=True, help_text="Required")
    github_url = forms.URLField(max_length=200, required=False, help_text="Optional")

    class Meta:
        model = User
        fields = ("username", "display_name", "github_url", "password1", "password2")