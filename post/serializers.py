from django.db import models
from post.models import Post,Like,Comment
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
    published = serializers.DateTimeField(source="date", read_only=True, allow_null=True)
    author = AuthorSerializer(source="get_author")
    object = serializers.CharField(source="get_post_id", required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['id', 'type', 'comment', 'contentType', 'published', 'author', 'object']

    def create(self, validated_data):
        post_id = self.context["post_id"]
        author_id = validated_data["get_author"]["get_url"].split("/")[-1]
        post = Post.objects.get(postID=post_id)
        author = Author.objects.get(authorID=author_id)
        if "date" in validated_data:
            if validated_data["date"] is not None:
                date = validated_data["date"]
            else:
                date = datetime.now(timezone.utc).astimezone().isoformat()
        else:
            date = datetime.now(timezone.utc).astimezone().isoformat()
        content = validated_data["get_content"]
        contentType = validated_data["contentType"]
        if "get_id" in validated_data:
            commentID = validated_data["get_id"].split("/")[-1]
            return Comment.objects.create(commentID=commentID, postID=post, authorID=author, date=date, content=content, contentType=contentType)
        else:
            return Comment.objects.create(postID=post, authorID=author, date=date, content=content, contentType=contentType)

class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="get_url", allow_null=True)
    type = serializers.CharField(default="post", read_only=True)
    author = AuthorSerializer(source="ownerID")
    categories = serializers.ListField(child=serializers.CharField(), source="get_categories", allow_null=True)
    count = serializers.IntegerField(source="get_comment_count", allow_null=True)
    comments = serializers.CharField(source="get_comment_url", allow_null=True)
    commentsSrc = serializers.SerializerMethodField(method_name="get_comments_src") #serializers.DictField(source="get_comments", allow_null=True, required=False) # CommentSerializer(source="get_comments", many=True, allow_null=True, required=False) #CommentSerializer(source="get_comments", many=True, allow_null=True, required=False)
    published = serializers.DateTimeField(source="date", allow_null=True)
    visibility = serializers.CharField(source="get_visibility")
    unlisted = serializers.BooleanField(source="is_unlisted")
    class Meta:
        model = Post
        fields = ['type', 'id', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'unlisted']

    def get_comments_src(self, obj):
        return {"type": "comments", "page": 1, "size": 5, "post": obj.get_url(), "id": obj.get_comment_url(), "comments": CommentSerializer(obj.get_comments(), many=True, allow_null=True, required=False).data}

    def create(self, validated_data):
        # print(validated_data)
        if validated_data["ownerID"]["get_url"].endswith("/"):
            ownerID = validated_data["ownerID"]["get_url"].split("/")[-2]
        else:
            ownerID = validated_data["ownerID"]["get_url"].split("/")[-1]
        ownerAuthor = Author.objects.get(authorID=ownerID)
        if "date" in validated_data:
            if validated_data["date"] is not None:
                date = validated_data["date"]
            else:
                date = datetime.now(timezone.utc).astimezone().isoformat()
        else:
            date = datetime.now(timezone.utc).astimezone().isoformat()
        title = validated_data["title"]
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
        url = validated_data["get_url"]
        #print("url: " + url)
        if url is not None:
            # If an id was given use it to create the post
            postID = url.split("/")[-1]
            # print("id: " + postID)
            if origin is None:
                # For brand new posts generate an origin
                post = Post.objects.create(postID=postID, ownerID=ownerAuthor, date=date, title=title, description=description, contentType=contentType, content=content, categories=categories, isPublic=isPublic, isListed=isListed, hasImage=hasImage)
                post.origin = post.get_url()
            else:
                # For reshared posts accept the origin
                post = Post.objects.create(postID=postID, ownerID=ownerAuthor, date=date, title=title, origin=origin, description=description, contentType=contentType, content=content, categories=categories, isPublic=isPublic, isListed=isListed, hasImage=hasImage)
        else:
            # If no id was given generate a new one
            if origin is None:
                # For brand new posts generate an origin
                post = Post.objects.create(ownerID=ownerAuthor, date=date, title=title, description=description, contentType=contentType, content=content, categories=categories, isPublic=isPublic, isListed=isListed, hasImage=hasImage)
                post.origin = post.get_url()
            else:
                # For reshared posts accept the origin
                post = Post.objects.create(ownerID=ownerAuthor, date=date, title=title, origin=origin, description=description, contentType=contentType, content=content, categories=categories, isPublic=isPublic, isListed=isListed, hasImage=hasImage)

        # Generate a new source for all new posts
        post.source = post.get_url()
        post.save()
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.description = validated_data.get("description", instance.description)
        instance.contentType = validated_data.get("contentType", instance.contentType)
        if "categories" in validated_data.keys():
            instance.categories = ";".join(validated_data.get("get_categories"))
        if "get_visibility" in validated_data.keys():
            if validated_data["get_visibility"].lower() == "public":
                instance.isPublic = True
            else:
                instance.isPublic = False
        if "is_unlisted" in validated_data.keys():
            if not validated_data["is_unlisted"]:
                instance.isListed = True
            else:
                instance.isListed = False
        if "image" in instance.contentType:
            instance.hasImage = True
        else:
            instance.hasImae = False
        instance.save()
        return instance

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
