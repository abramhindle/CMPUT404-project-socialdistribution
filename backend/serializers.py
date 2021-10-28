from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Author, Post, Comment, Like

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author", read_only=True)
    id = serializers.URLField(source="get_id", read_only=True)
    displayName = serializers.CharField(source="display_name")
    github = serializers.URLField(source="github_url", allow_blank=True)
    # profileImage = serializers.URLField(source="profile_image", allow_blank=True)

    class Meta:
        model = Author
        fields = ("type","id","host","displayName","url","github","profile_image")
    
    """
    Method used to update the model
    """
    def update(self, instance, validated_data):
        instance.github_url = validated_data.get("github_url", instance.github_url)
        instance.display_name = validated_data.get("display_name", instance.display_name)
        instance.profile_image = validated_data.get("profile_image", instance.profile_image)
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
    author = AuthorSerializer(read_only=False)

    class Meta:
        model = Comment
        fields = ("type", "author", "comment", "contentType", "published", "id")

    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        if author_data:
            author = Author.objects.get_or_create(**author_data)[0]
            validated_data['author'] = author
        validated_data.pop('id', None)
        comment = Comment.objects.create(**validated_data)
        return comment


class PostSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="post", read_only=True)
    id = serializers.URLField(source="get_id", read_only=True)
    content_type = serializers.CharField()
    # https://www.tomchristie.com/rest-framework-2-docs/api-guide/serializers#dealing-with-nested-objects
    comments = CommentSerializer(many=True, required=False)
    author = AuthorSerializer(read_only=False)
    class Meta:
        model = Post
        fields = ("type","id","url","title","source",
                  "origin","description","content_type",
                  "content","author","comments",
                  "published","visibility","unlisted")

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.source = validated_data.get("source", instance.source)
        instance.origin = validated_data.get("origin", instance.origin)
        instance.description = validated_data.get("description", instance.description)
        instance.content_type = validated_data.get("content_type", instance.content_type) 
        instance.content = validated_data.get("content", instance.content) 
        instance.published = validated_data.get("published", instance.published)
        instance.visibility = validated_data.get("visibility", instance.visibility)
        instance.unlisted = validated_data.get("unlisted", instance.unlisted)
        instance.save()
        return instance

    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        if author_data:
            author = Author.objects.get_or_create(**author_data)[0]
            validated_data['author'] = author

        post = Post.objects.create(**validated_data)
        return post

class PostsLikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="Like", read_only=True)
    # https://www.tomchristie.com/rest-framework-2-docs/api-guide/serializers#dealing-with-nested-objects
    summary = serializers.CharField()
    author = AuthorSerializer(many=False, required=True)
    object = serializers.URLField(source="get_object", read_only=True)
    class Meta:
        model = Like
        fields = ("summary","type","author","object")

    def create(self, validated_data):
        like = Like.objects.create(**validated_data)
        return like
class CommentsLikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="Like", read_only=True)
    # https://www.tomchristie.com/rest-framework-2-docs/api-guide/serializers#dealing-with-nested-objects
    summary = serializers.CharField()
    author = AuthorSerializer(many=False, required=True)
    object = serializers.URLField(source="get_object", read_only=True)
    class Meta:
        model = Like
        fields = ("summary","type","author","object")

    def create(self, validated_data):
        like = Like.objects.create(**validated_data)
        return like