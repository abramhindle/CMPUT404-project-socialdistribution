from rest_framework import serializers
from presentation.models import Post, Author



class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['type', 'title', 'id', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'size', 'comments', 'published', 'visibility', 'unlisted']

