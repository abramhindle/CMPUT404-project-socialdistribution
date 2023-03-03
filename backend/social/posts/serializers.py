from rest_framework import serializers
from .models import *
from author.serializers import AuthorSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
# pip install drf-base64
from drf_base64.fields import Base64ImageField

class PostSerializer(WritableNestedModelSerializer):
    type = serializers.CharField(default="post",source="get_api_type",read_only=True)
    id = serializers.CharField(source="get_public_id", read_only=True)
    count = serializers.IntegerField(source="count_comments", read_only=True)
    comments = serializers.URLField(source="get_comments_source", read_only=True)
    author = AuthorSerializer()
    # count = serializers.IntegerField(source='sget_comment_count')
#    source = serializers.URLField(default="",max_length=500)  # source of post
#    origin = serializers.URLField(default="",max_length=500)  # origin of post
    categories = serializers.SerializerMethodField(read_only=True)
        
    def get_categories(self, instance):
        categories_list = instance.categories.split(",")
        return [category for category in categories_list]
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.content = validated_data.get('content', instance.content)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.published = validated_data.get('published', instance.published)
        return instance
    
    def create(self, instance, validated_data):
        updated_author = AuthorSerializer.extract_and_upcreate_author(validated_data, author_id=self.context.get('author_id'))
        categories = ' '.join(validated_data.get('categories'))
        print("categories", categories)
        validated_data.pop('categories')
        return Post.objects.create(**validated_data, categories = categories, author=updated_author)

    def to_representation(self, instance):
            id = instance.get_public_id()
            id = id[:-1] if id.endswith('/') else id
            return {
                **super().to_representation(instance),
                'id': id
            }
    class Meta:
        model = Post
        fields = [
            'type', 
            'title', 
            'id', 
            #'source', 
            #'origin', 
            'description',
            'contentType',
            'content',
            'author',
            'categories',
            'count',
            'comments',
            'published',
            'visibility',
            #'unlisted',
            #'is_github'
        ]

class CommentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="comment",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    author = AuthorSerializer()
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
    id = serializers.URLField(source="get_public_id",read_only=True)
    author = AuthorSerializer()
    class Meta:
        model = Like
        fields = [
            "summary",
            "type",
            "author",
            "object",
            "id",
        ]

class ImageSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="post",source="get_api_type",read_only=True)
    image = Base64ImageField()
    author = AuthorSerializer()
    id = serializers.URLField(source="get_public_id",read_only=True)
    class Meta:
        model = Post
        fields = [
            "type",
            "id",
            "author",
            "image",
            "visibility",
        ]