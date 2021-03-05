from rest_framework import serializers
from .models import *
# import json
# from uuid import UUID

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['authorID', 'email', 'username', 'password', 'github']

    def save(self):
        author = Author(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            github=self.validated_data['github']
        )
        password = self.validated_data['password']
        author.set_password(password)
        author.save()
        return author


class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type', required=False)
    id = serializers.CharField(source='get_id', required=False)
    host = serializers.URLField(source='get_host', required=False)
    displayName = serializers.CharField(source='username', required=False)
    url = serializers.CharField(source='get_id', required=False)

    class Meta:
        model = Author
        fields = ['type', 'id', 'host', 'displayName', 'url', 'github', 'authorID']


class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='get_post_id', required=False)
    comments = serializers.URLField(source='get_comments_url', required=False)
    type = serializers.CharField(source='get_type', required=False)

    def to_representation(self, instance):
        response = super(PostSerializer, self).to_representation(instance)
        author = Author.objects.get(authorID=instance.authorID)
        author_serializer = AuthorSerializer(author)
        response['author'] = author_serializer.data # add author data
        response['comment_list'] = instance.comment_list[:5]

        return response

    class Meta:
        model = Post
        fields = ['type', 'title', 'id', 'authorID', 'postID', 'source', 'origin', 'description', 'contentType',
            'content', 'count', 'comments', 'comment_list','published', 'visibility', 'unlisted']

# class FriendRequestSerializer(serializers.ModelSerializer):
#     #summary = serializers.SerializerMethodField("get_summary",required=False)
#     object = serializers.CharField(source='get_author',required=False) # the user being followed
#     actor = serializers.CharField(source='get_actor',required=False) # the new follower
#     type = serializers.CharField(source='get_type',required=False)
#     """ terminology: Greg wants to follow Lara:
#     Greg is the actor
#     Lara is the object """
#
#     class Meta:
#         model = FriendRequest
#         fields = ['type', 'summary', 'actor', 'object']
#
#     def to_representation(self, instance):
#         response = super(FriendRequestSerializer, self).to_representation(instance)
#         actor = Author.objects.get(authorID = instance.new_follower_ID) # the new follower
#         actor_serializer = AuthorSerializer(actor)
#         object = Author.objects.get(authorID = instance.object) # the user being followed
#         object_serializer = AuthorSerializer(object)
#         del response['new_follower_ID']
#         response['summary'] = actor.username + "wants to follow" + object.username
#         response['actor'] = author_serializer.data
#         response['object'] = object_serializer.data
#         return response

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='get_comment_id', required=False)
    author = serializers.CharField(source='get_author',required=False)
    type = serializers.CharField(source='get_type',required=False)
    def to_representation(self, instance):
        response = super(CommentSerializer, self).to_representation(instance)
        #get author from author ID
        author = Author.objects.get(authorID = instance.author_write_comment_ID)
        author_serializer = AuthorSerializer(author)
        response['postID'] = str(response['postID'])
        response['commentID'] = str(response['commentID'])
        response['author'] = author_serializer.data # add author data
        return response

    class Meta:
        model = Comment
        fields = ['type','author','comment','contentType','published','commentID','author_write_article_ID','author_write_comment_ID','postID','id']
    def get_author(self,instance):
        #get author from author ID
        author_data = Author.objects.get(authorID = instance.author_write_comment_ID)
        author_serializer = AuthorSerializer(author_data)
        author = author_serializer.data
        return author


class InboxSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type', required=False)
    author = serializers.CharField(source='get_author')

    class Meta:
        model = Inbox
        fields = ['type', 'author', 'items']


class LikePostSerializer(serializers.ModelSerializer):
    object = serializers.URLField(source='get_like_model',required=False)
    author = serializers.CharField(source='get_author',required=False)
    summary = serializers.SerializerMethodField("get_summary")
    at_context = serializers.URLField(source='get_at_context',required=False)

    def to_representation(self, instance):
        response = super(LikePostSerializer, self).to_representation(instance)
        #get author from author ID
        author_like = Author.objects.get(authorID = instance.author_like_ID)
        author_like_serializer = AuthorSerializer(author_like)
        del response['author_write_article_ID']
        del response['postID']
        del response['author_like_ID']
        response['author'] = author_like_serializer.data # add author data
        response['summary'] = author_like.username + " likes your post"
        return response

    class Meta:
        model = LikePost
        fields = ['at_context','type','author','summary','published','author_write_article_ID','author_like_ID','postID','object']

    def get_summary(self,instance):
        id = instance.author_like_ID
        author_like = Author.objects.get(authorID = id)
        summary = author_like.username + " likes your post"
        return summary

class LikeCommentSerializer(serializers.ModelSerializer):
    object = serializers.URLField(source='get_like_model',required=False)
    #author = serializers.CharField(source='get_author',required=False)
    #summary = serializers.SerializerMethodField("get_summary")
    #author_write_comment_ID = serializers.SerializerMethodField("get_author_write_comment_ID")
    at_context = serializers.URLField(source='get_at_context',required=False)

    def to_representation(self, instance):
        response = super(LikeCommentSerializer, self).to_representation(instance)
        #get author from author ID
        author_like = Author.objects.get(authorID = instance.author_like_ID)
        author_like_serializer = AuthorSerializer(author_like)
        del response['author_write_article_ID']
        del response['commentID']
        del response['postID']
        del response['author_like_ID']
        response['author'] = author_like_serializer.data # add author data
        response['summary'] = author_like.username + " likes your comment"
        #response['postID'] = str(response["postID"]) # convert UUID to string
        return response

    class Meta:
        model = LikeComment
        fields = ['at_context','type','published','author_write_article_ID','author_like_ID','commentID','postID','object']

    def get_summary(self,instance):
        author_like = Author.objects.get(authorID = instance.author_like_ID)
        summary = author_like.username + " likes your comment"
        return summary
    def get_author(self,instance):
        author_like = Author.objects.get(authorID = instance.author_like_ID)
        author_like_serializer = AuthorSerializer(author_like)
        return author_like_serializer.data
    def get_author_write_comment_ID(self,instance):
        #get comment
        comment = instance.commentID
        #get the author who write the comment
        author_write_comment_ID = comment.author_write_comment_ID

        return author_write_comment_ID

class LikedSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type', required=False)
    def to_representation(self, instance):
        response = super(LikedSerializer, self).to_representation(instance)
        del response['authorID']
        return response

    class Meta:
        model = Liked
        fields = ['type','authorID','items']

# class UUIDEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, UUID):
#             # if the obj is uuid, we simply return the value of uuid
#             return obj.hex
#         return json.JSONEncoder.default(self, obj)
