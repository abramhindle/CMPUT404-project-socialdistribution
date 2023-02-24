from django import forms
from .models import *

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['id','uploaded_img']