from .models import authorModel, postModel, accountRegistrationModel, commentModel
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Author Serializer
class AuthorSerializer(serializers.ModelSerializer):
  type = serializers.CharField(default='author')
  id = serializers.URLField(source='url')
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
  id = serializers.URLField(source='postID')
  author = AuthorSerializer(read_only=True, source='postAuthor')

  class Meta:
    model = postModel.Post
    fields = ['type', 'title', 'id', 'source', 'origin', 'description', 
        'contentType', 'content', 'author', 'categories', 'count', 
        # 'comments', 
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


# COMMENT SERIALIZER
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
      model = commentModel.Comment
      fields = ['content', 'contentType']

    # Allows account update/changes
    def create(self, validData):
        comment_ = commentModel.Comment(**validData,
                                   post_id=self.context.get('post_id'),
                                   Comment_authorID=self.context.get('request').user)
        url = f"{self.context.get('request').build_absolute_uri()}/{comment_.commentID}"
        comment_.url = url
        comment_.save()
        return comment_


# Inbox Serializer ////* Needs to be completed for next sprint */////
# class InboxSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = inboxModel.Inbox
#     fields = ['author_id', 'messageType', 'items']
