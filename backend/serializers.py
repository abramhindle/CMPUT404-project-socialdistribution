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
        fields = ("type","id","host","displayName","url","github")
    
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

class CommentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="comment", read_only=True)
    id = serializers.URLField(source="get_id", read_only=True)
    contentType = serializers.CharField(source="content_type")

    class Meta:
        model = Comment
        fields = ("type","id","contentType","comment","published")


class PostSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="post", read_only=True)
    id = serializers.URLField(source="get_id", read_only=True)
    contentType = serializers.CharField(source="content_type")
    # https://www.tomchristie.com/rest-framework-2-docs/api-guide/serializers#dealing-with-nested-objects
    comments = CommentSerializer(many=True, required=False)
    class Meta:
        model = Post
        fields = ("type","id","url","title","source",
                  "origin","description","contentType",
                  "content","author","comments",
                  "published","visibility","unlisted")

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.source = validated_data.get("source", instance.source)
        instance.origin = validated_data.get("origin", instance.origin)
        instance.description = validated_data.get("description", instance.description)
        instance.content_type = validated_data.get("content_type", instance.content_type) 
        instance.published = validated_data.get("published", instance.content_type)
        instance.visibility = validated_data.get("visibility", instance.visibility)
        instance.unlisted = validated_data.get("unlisted", instance.unlisted)
        instance.save()

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post
