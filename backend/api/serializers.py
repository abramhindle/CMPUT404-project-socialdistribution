from .models import authorModel, postModel, inboxModel, likeModel, accountRegistrationModel, commentModel
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

# Auth Token Serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

# Registration Serializer
class RegistrationSerializer(serializers.ModelSerializer):
  class Meta:
    model = accountRegistrationModel.accountRequest
    fields = ['username','password', 'displayName','github', 'host']

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
  author = AuthorSerializer(read_only=True)

  class Meta:
    model = postModel.Post
    fields = ['type', 'title', 'id', 'source', 'origin', 'description', 
        'contentType', 'content', 'author', 'categories', 'count', 'comments', 
        'published', 'visibility', 'unlisted']

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
  author = AuthorSerializer(read_only=True)

  class Meta:
      model = commentModel.Comment
      fields = ['type', 'author', 'comment', 'contentType', 'published', 'id'] 

# Like Serializer
class LikeSerializer(serializers.ModelSerializer):
  author = AuthorSerializer(read_only=True)
  
  class Meta:
      model = likeModel.Like
      fields = ['context', 'summary', 'type', 'author', 'object'] 

# Inbox Serializer
class InboxSerializer(serializers.ModelSerializer):
  class Meta:
    model = inboxModel.Inbox
    fields = ['type', 'author', 'items']
