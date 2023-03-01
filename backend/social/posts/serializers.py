from rest_framework import serializers
from .models import Post, Comment
from author.serializers import AuthorSerializer


class PostSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="post",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    count = serializers.IntegerField(source="count_comments", read_only=True)
    comments = serializers.URLField(source="get_comments_source", read_only=True)
    # categories = serializers.ListSerializer(child=serializers.CharField())
    author = AuthorSerializer()
    # count = serializers.IntegerField(source='sget_comment_count')
#    source = serializers.URLField(default="",max_length=500)  # source of post
#    origin = serializers.URLField(default="",max_length=500)  # origin of post
    categories = serializers.SerializerMethodField(read_only=True)

    def get_categories(self, instance):
        categories_list = instance.categories.split(",")
        return [category for category in categories_list]
    
    class Meta:
        model = Post
        fields = [
            'type', 
            'title', 
            'id', 
            #'url',
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
