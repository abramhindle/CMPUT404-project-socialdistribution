from .models import author, post
from rest_framework import serializers

##############################################
# serializers is for serialize the model into json format
# This format is acceptable for http
##################################################


# serializer for post model into json representation
class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = post
    fields = ['post_id', 'origin_post_url', 'author_id', 'title', 'description', 'content', 'contentType', 'visibility'
    , 'unlisted', 'published', 'url']