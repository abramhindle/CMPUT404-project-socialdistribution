from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Author, Post, Comment

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author", read_only=True)
    id = serializers.URLField(source="get_id", read_only=True)
    displayName = serializers.CharField(source="display_name")
    github = serializers.URLField(source="github_url")

    class Meta:
        model = Author
        fields = ('type','id','host','displayName','url','github')
    
    """
    Method used to update the model
    """
    def update(self, instance, validated_data):
        instance.github_url = validated_data.get("github_url", instance.github_url)
        instance.display_name = validated_data.get("display_name", instance.display_name)
        instance.save()
        return instance

    def validate_github_url(self, value):
        if value:
            value = value[value.find("//") + 2:]
            value = value[:value.find("/")]
            if not value.contains("github.com"):
                raise ValidationError(_("Author's github url must be a github url"))
        return value

        

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','url','title','source','origin','description',
                  'contentType','content','author','published','visibility','unlisted')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','contentType','comment','published')
