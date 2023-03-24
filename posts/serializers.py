from rest_framework import serializers
from .models import *
from .models import Post
from author.serializers import AuthorSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_base64.fields import Base64ImageField
import uuid 

class PostSerializer(WritableNestedModelSerializer):
    type = serializers.CharField(default="post",source="get_api_type",read_only=True)
    id = serializers.CharField(source="get_public_id", read_only=True)
    count = serializers.IntegerField(read_only=True, default=0)
    comments = serializers.URLField(source="get_comments_source", read_only=True)
    commentsSrc = serializers.JSONField(read_only=True)
    author = AuthorSerializer(required=False)
    source = serializers.URLField(source="get_source", read_only=True, max_length=500)  # source of post
    origin = serializers.URLField(source="get_origin", read_only=True, max_length=500)  # origin of post
    categories = serializers.CharField(max_length=300, default="")
    
    def create(self, validated_data):
        author = AuthorSerializer.extract_and_upcreate_author(validated_data, author_id=self.context["author_id"])
        id = validated_data.pop('id') if validated_data.get('id') else None
        if not id:
            id = self.context["id"]
        post = Post.objects.create(**validated_data, author = author, id = id)
        return post

    def to_representation(self, instance):
        id = instance.get_public_id()
        categories_list = instance.categories.split(",")
        comments_list = Comment.objects.filter(post=instance).order_by('-published')[0:5]
        commentsSrc = [CommentSerializer(comment,many=False).data for comment in comments_list]
        return {
            **super().to_representation(instance),
            'id': id,
            'categories':[category for category in categories_list],
            'commentsSrc': commentsSrc,
            'count': len(commentsSrc)
        }
            
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
            'categories',
            'count',
            'comments',
            'commentsSrc',
            'published',
            'visibility',
            #'unlisted',
            #'is_github'
        ]

class CommentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="comment",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    author = AuthorSerializer()

    def create(self, validated_data):
        author = AuthorSerializer.extract_and_upcreate_author(validated_data,author_id=self.context["author_id"])
        id = validated_data.pop('id') if validated_data.get('id') else None
        
        if not id:
            id = self.context["id"]
        comment = Comment.objects.create(**validated_data, author = author, id = id, post=self.context["post"])
        comment.save()
        return comment

    class Meta:
        model = Comment
        fields = [
            'type', 
            'author',
            'comment',
            'contentType',
            'published',
            'id',       
        ]

class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="like",source="get_api_type",read_only=True)
    author = AuthorSerializer(required=True)
    summary = serializers.CharField(source="get_summary", read_only=True)

    def create(self, validated_data):
        author = AuthorSerializer.extract_and_upcreate_author(validated_data, author_id=self.context["author_id"])
       
        if Like.objects.filter(author=author, object=validated_data.get("object")).exists():
            return "already liked"
        else:
            id = str(uuid.uuid4())
            like = Like.objects.create(**validated_data, author=author, id = id)
            like.save()
            return like

    class Meta:
        model = Like
        fields = [
            "summary",
            "type",
            "author",
            "object",
        ]

class ImageSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="post",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    author = AuthorSerializer(required=False)
    image = Base64ImageField()
    
    def create(self, validated_data):
        author = AuthorSerializer.extract_and_upcreate_author(validated_data, author_id=self.context["author_id"])
        id = validated_data.pop('id') if validated_data.get('id') else None
        if not id:
            id = self.context["id"]
        post = Post.objects.create(**validated_data, author = author, id = id)
        return post

    class Meta:
        model = Post
        fields = [
            "contentType",
            "type",
            "id",
            "author",
            "image",
            "visibility",
        ]