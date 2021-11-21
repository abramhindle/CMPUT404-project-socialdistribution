# Implementation of serializers from the tutorial: https://www.django-rest-framework.org/tutorial/1-serialization/

from rest_framework import serializers
from apps.core.serializers import AuthorSerializer
from apps.posts.models import Comment, Like, Post

class PostSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="post", read_only=True)
    id = serializers.CharField(source="get_post_id", read_only=True)
    contentType = serializers.ChoiceField(choices=Post.ContentTypeEnum.choices, default=Post.ContentTypeEnum.PLAIN)
    author = AuthorSerializer(read_only=True)
    visibility = serializers.ChoiceField(choices=Post.VisibilityEnum.choices, default=Post.VisibilityEnum.PUBLIC)
    count = serializers.IntegerField(source="get_comments_count", read_only=True)
    comments = serializers.CharField(source="get_comments_uri", read_only=True)

    class Meta:
        model = Post
        fields = [
            'type', 
            'title', 
            'id', 
            'source',
            'origin',
            'description',
            'contentType',
            'content',
            'author',
            # 'categories',
            'count',
            'comments',
            'published',
            'visibility',
            'unlisted'
        ]

    def get_comments_url(self, obj):
        host = self.context.get("host")
        print(self.context)
        if (host):
            return host + "/author/" + str(obj.author.id) + "/post/" + str(obj.post.id) + "comments/"
        return None

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_id')
    type = serializers.CharField(default="comment", read_only=True)
    contentType = serializers.ChoiceField(choices=Post.ContentTypeEnum.choices, default=Post.ContentTypeEnum.PLAIN)
    author = AuthorSerializer(read_only=True)

    def get_id(self, obj):
        host = self.context.get("host")
        if (host):
            return host + "/author/" + str(obj.author.id) + "/post/" + str(obj.post.id) + "/comments/" + str(obj.id)
        return None

    class Meta:
        model = Comment
        fields = [
            'type',
            'id', 
            'author',
            'comment',
            'contentType',
            'published',
        ]


class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="like", read_only=True)
    author = AuthorSerializer(read_only=True)
    object = serializers.SerializerMethodField('get_object')

    def get_object(self, obj):
        host = self.context.get("host")
        if (host):
            if (obj.post):
                return host + "/author/" + str(obj.post.author.id) + "/post/" + str(obj.post.id)
            elif (obj.comment):
                return host + "/author/" + str(obj.comment.post.author.id) + "/post/" + str(obj.comment.post.id) + "/comment/" + str(obj.comment.id)
        
        return None

    class Meta:
        model = Like
        fields = [
            'summary', 
            'type',
            'author',
            'object',
        ]