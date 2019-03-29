from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Follow, FollowRequest, Post, Comment, Category, Viewer, WWUser
import base64
from django.urls import reverse
from django.contrib.sites.models import Site
from dispersal.settings import SITE_URL


class WWUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WWUser
        fields = ('url',)


# TODO: is general posting succcess messages correct, or should be it be like example json?
class UserSerializer(serializers.HyperlinkedModelSerializer):
    firstName = serializers.CharField(source='first_name', default='')
    lastName = serializers.CharField(source='last_name', default='')
    displayName = serializers.CharField(source='username')
    password1 = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    github = serializers.URLField(allow_blank=True, required=False)
    host = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField('get_absolute_url', read_only=True)
    url = serializers.SerializerMethodField('get_absolute_url', read_only=True)
    email = serializers.EmailField(default='')

    class Meta:
        model = User
        write_only_fields = ('password1', 'password2')
        fields = ('id', 'displayName', 'url', 'host', 'github', 'firstName', 'lastName', 'bio', 'email', 'password1', 'password2')

    def get_host(self, obj):
        return SITE_URL

    def get_absolute_url(self, obj):
        author_path = 'author/' + str(obj.id)
        return self.get_host(obj) + author_path

    def validate(self, data):
        if self.context['create'] and ('password1' not in data.keys() or 'password2' not in data.keys()):
            raise serializers.ValidationError("Please enter a password")
        if self.context['create'] and (len(data['password1']) < 1 or len(data['password2']) < 1):
            raise serializers.ValidationError("Please enter a password")
        if self.context['create'] and data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match.')
        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        if 'github' in validated_data.keys():
            github = validated_data['github']
        else:
            github=""
        if 'bio' in validated_data.keys():
            bio = validated_data['bio']
        else:
            bio = ""
        user = User(
            username=validated_data['username'],
            github=github,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            bio=bio,
            email=validated_data['email'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        url = self.get_absolute_url(user)
        ww_user = WWUser(url=url, local=True, user_id=user.id)
        ww_user.save()
        return user

    def to_user_model(self):
        user = User(username=self.initial_data['displayName'],
                    github=self.initial_data.get('github', ''),
                    first_name=self.initial_data.get('firstName', ''),
                    last_name=self.initial_data.get('lastName', ''),
                    bio=self.initial_data.get('bio', ''),
                    id=self.initial_data['id'],
                    host=self.initial_data['host'])
        return user



class FollowSerializer(serializers.HyperlinkedModelSerializer):
    # The one who is following
    follower = WWUserSerializer(read_only=True)
    # The one who is being followed.
    followee = WWUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('followee','follower')

    def create(self, validated_data):
        user = WWUser.objects.get(url=self.context['followee'].url)
        other = WWUser.objects.get(url=self.context['follower'].url)
        follow = Follow.objects.create(followee=user, follower=other)
        follow.save()
        return follow


class FollowRequestSerializer(serializers.HyperlinkedModelSerializer):
    # The one wishing to be followed back
    requester = WWUserSerializer(read_only=True)
    # The one who will decide to follow the requester back
    requestee = WWUserSerializer(read_only=True)

    class Meta:
        model = FollowRequest
        fields = ('requester', 'requestee')

    def create(self, validated_data):
        user = WWUser.objects.get(url=self.context['requestee'].url)
        other = WWUser.objects.get(url=self.context['requester'].url)
        req = FollowRequest.objects.create(requestee=user, requester=other)
        req.save()
        return req


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = WWUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("author", "comment", "contentType", "published", "id")

    def create(self, validated_data):
        post_id = self.context['post_id']
        post = Post.objects.get(pk=post_id)
        user = WWUser.objects.get(url=self.context['user'].url)
        comment = Comment.objects.create(parent_post=post, author=user, **validated_data)
        return comment


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('categories')


class VisibleTo(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value

class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(required=False, many=True, read_only=True)
    categories = serializers.SlugRelatedField(
        many=True,
        queryset=Category.objects.all(),
        slug_field='category',
        required=False,
        read_only=False
    )
    visibleTo = VisibleTo(required=False, many=True, read_only=False)

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'source', 'origin', 'description', 'author', 'categories', 'contentType', 'content',
            'published',
            'visibility', 'visibleTo', 'unlisted', 'comments')

    def create(self, validated_data):

        if 'categories' in validated_data.keys():
            categories_data = validated_data.pop('categories')
        else:
            categories_data = []

        if ('visibleTo' in validated_data.keys()):
            visible_to_data = validated_data.pop('visibleTo')

        user = User.objects.get(username=self.context['user'].username)
        post = Post.objects.create(author=user, **validated_data)

        for category_data in categories_data:
            post.categories.add(category_data)

        # apparently create calls .save() implicitly
        return post
