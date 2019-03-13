from django.forms import ModelForm
from .models import User


class UserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = []
