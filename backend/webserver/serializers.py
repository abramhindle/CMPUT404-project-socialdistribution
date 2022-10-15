from distutils.command.config import LANG_EXT
from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fiels = ('display_name','profile_image','github_handle')