from rest_framework import serializers
from presentation.models import Likes



class LikesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Likes
		fields = ['type', 'context','author','summary','post_object','comment_object']

