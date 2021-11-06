from .models import authorModel, postModel, accountRegistrationModel, commentModel
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Author Serializer
class AuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = authorModel.Author
    fields = ['type', 'id', 'host', 'displayName', 'url', 'github', 'profileImage']

  # Allows account update/changes
  def update(self, instance, validData):
    instance.displayName = validData.get('displayName', instance.displayName)
    instance.github = validData.get('github', instance.github)
    instance.save()
    return instance

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
  author = AuthorSerializer(read_only=True)

  class Meta:
    model = postModel.Post
    fields = ['type', 'title', 'id', 'source', 'origin', 'description', 
        'contentType', 'content', 'author', 'categories', 'count', 'comments', 
        'published', 'visibility', 'unlisted']

# Auth Token Serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

class RegistrationSerializer(serializers.ModelSerializer):
  class Meta:
    model = accountRegistrationModel.accountRequest
    fields = ['username','password', 'displayName','github', 'host']

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
  author = AuthorSerializer(read_only=True)

  class Meta:
      model = commentModel.Comment
      fields = ['type', 'author', 'comment', 'contentType', 'published', 'id'] 

# Inbox Serializer ////* Needs to be completed for next sprint */////
# class InboxSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = inboxModel.Inbox
#     fields = ['author_id', 'messageType', 'items']
