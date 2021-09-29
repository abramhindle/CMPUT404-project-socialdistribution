from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # type is only provided to satisfy API format
    type = serializers.CharField(default="post", source="get_api_type")
    # public id should be the full url
    id = serializers.CharField(source="get_public_id")
    title = serializers.CharField(source="title")



    class Meta:
        model = Post
        # show these fields in response
        fields = [
            'type', 
            'id', 
            'title', 
            'source', 
            'origin', 
            'description'
        ]

