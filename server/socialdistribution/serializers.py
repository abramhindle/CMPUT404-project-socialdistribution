from rest_framework import serializers
from .models import *

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
        fields = ['type', 'id', 'host', 'displayName', 'url', 'github']


class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='get_post_id', required=False)
    comments = serializers.URLField(source='get_comments_url', required=False)
    type = serializers.CharField(source='get_type', required=False)

    def to_representation(self, instance):
        response = super(PostSerializer, self).to_representation(instance)
        author = Author.objects.get(authorID=instance.authorID)
        author_serializer = AuthorSerializer(author)
        del response['authorID']
        del response['postID']
        response['author'] = author_serializer.data # add author data

        return response

    class Meta:
        model = Post
        fields = ['type', 'title', 'id', 'authorID', 'postID', 'source', 'origin', 'description', 'contentType',
            'content', 'count', 'comments', 'published', 'visibility', 'unlisted']

# class FriendRequestSerializer(serializers.ModelSerializer):
#     summary = serializers.CharField(max_length=20)
#     actor = AuthorSerializer()
#     object = FriendSerializer()
#     """ terminology: Greg wants to follow Lara
#     Greg is the actor
#     Lara is the object """
#
#     class Meta:
#         model = FriendshipRequest
#         fields = ['type', 'summary', 'actor', 'object']
#
#     def sendRequest(self, instance):
#         sender = self.validated_data.get('sender')
#         friend_serializer = FriendSerializer(data=sender)
#         friend_serializer.is_valid()
#         friend_serializer.save()
#         actor = Friend.objects.get(id=requestor_data.get('id'))
#
#         receiver = self.validated_data.get('receiver')
#         object = get_object_or_404(Profile, id=friend_data.get('id'))
#         if object not in Follow.objects.following(instance.authorID):
#             Follow.objects.add_follower(instance.authorID, object)

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='get_comment_id', required=False)
    author = serializers.CharField(source='get_author',required=False)
    type = serializers.CharField(source='get_type',required=False)
    def to_representation(self, instance):
        response = super(CommentSerializer, self).to_representation(instance)
        #get author from author ID
        author = Author.objects.get(authorID = instance.author_write_comment_ID)
        author_serializer = AuthorSerializer(author)
        del response['author_write_article_ID']
        del response['postID']
        del response['commentID']
        del response['author_write_comment_ID']
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
    
    def to_representation(self, instance):
        response = super(LikeCommentSerializer, self).to_representation(instance)
        #get author from author ID
        author_like = Author.objects.get(authorID = instance.author_like_ID)
        author_like_serializer = AuthorSerializer(author_like)
        del response['author_write_article_ID']
        #del response['author_write_comment_ID']
        del response['commentID']
        del response['postID']
        del response['author_like_ID']
        response['author'] = author_like_serializer.data # add author data
        response['summary'] = author_like.username + " likes your comment"
        #response['postID'] = str(response["postID"]) # convert UUID to string
        return response

    class Meta:
        model = LikeComment
        #fields = ['at_context','type','author','summary','published','author_write_article_ID','author_write_comment_ID','author_like_ID','commentID','postID','object']
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
