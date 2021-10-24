from django.db import models
from .models import Post,Like,Comment
from rest_framework import serializers
from author.serializers import AuthorSerializer
from author.models import Author
from datetime import datetime, timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="get_id", read_only=True)
    type = serializers.CharField(default="comment", read_only=True)
    comment = serializers.CharField(source="get_content")
    published = serializers.DateTimeField(source="get_date", read_only=True)
    author = AuthorSerializer(source="get_author")

    class Meta:
        model = Comment
        fields = ['id', 'type', 'comment', 'contentType', 'published', 'author']

    def create(self, validated_data):
        post_id = self.context["post_id"]
        author_id = self.context["author_id"]
        post = Post.objects.get(postID=post_id)
        author = Author.objects.get(authorID=author_id)
        date = datetime.now(timezone.utc).astimezone().isoformat()
        content = validated_data["get_content"]
        contentType = validated_data["contentType"]
        return Comment.objects.create(postID=post, authorID=author, date=date, content=content, contentType=contentType)

class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="get_url")
    type = serializers.CharField(default="post", read_only=True)
    author = AuthorSerializer(source="ownerID")
    categories = serializers.ListField(child=serializers.CharField(), source="get_categories")
    count = serializers.IntegerField(source="get_comment_count")
    comments = serializers.CharField(source="get_comment_url")
    commentsSrc = CommentSerializer(source="get_comments", many=True, allow_null=True, required=False)
    published = serializers.DateTimeField(source="date")
    visibility = serializers.CharField(source="get_visibility")
    unlisted = serializers.BooleanField(source="is_unlisted")
    class Meta:
        model = Post
        fields = ['type', 'id', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'unlisted']

    def create(self, validated_data):
        author = validated_data["ownerID"]["get_url"].split("/")[-1]
        ownerID = Author.objects.get(authorID=author)
        date = validated_data["date"]
        title = validated_data["title"]
        source = validated_data["source"]
        origin = validated_data["origin"]
        description = validated_data["description"]
        contentType = validated_data["contentType"]
        content = validated_data["content"]
        categories = ";".join(validated_data["get_categories"])
        isPublic = False
        if validated_data["get_visibility"].lower() == "public":
            isPublic = True
        isListed = False
        if not validated_data["is_unlisted"]:
            isListed = True
        hasImage = False
        if "image" in contentType:
            hasImage = True
        postID = validated_data["get_url"].split("/")[-1]
        return Post.objects.create(postID=postID, ownerID=ownerID, date=date, title=title, source=source, origin=origin, description=description, contentType=contentType, content=content, categories=categories, isPublic=isPublic, isListed=isListed, hasImage=hasImage)


class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="like", read_only=True)
    author = AuthorSerializer(source="authorID")
    object = serializers.URLField(source="get_object_url")
    class Meta:
        model = Like
        fields = ['author', 'type', "@context", "summary", "object"]
        extra_kwargs = {
            # rename content to @content
            '@context': {'source': 'context'},
        }

    def create(self, validated_data):
        object = validated_data["get_object_url"]
        if "/comments/" in object:
            content_type = ContentType.objects.get(model="comment")
        else:
            content_type = ContentType.objects.get(model="post")
        objectID = object.split("/")[-1]
        authorID = validated_data["authorID"]["get_url"].split("/")[-1]
        author = Author.objects.get(authorID=authorID)
        summary = validated_data["summary"]
        context = validated_data["context"]
        return Like.objects.create(objectID=objectID, content_type=content_type, authorID=author, summary=summary, context=context)
