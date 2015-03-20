from django.db import models
# coding: utf-8  
from images.models import Image
from django import forms


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Image
        field = ('thumb')

    @staticmethod
    def createImage(profile, file):
        if profile.is_valid():
            profile.picture = file
            return profile.save()