from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Post, Comment, Category
import base64


class UserSerializer(serializers.HyperlinkedModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    displayName = serializers.CharField(source='username', validators=[UniqueValidator(User.objects.all())])
    password1 = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    github = serializers.URLField(allow_blank=True, required=False)
    email = serializers.EmailField()

    class Meta:
        model = User
        write_only_fields = ('password1', 'password2')
        fields = ('id', 'displayName', 'github', 'firstName', 'lastName', 'bio', 'email', 'password1', 'password2')

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
        return user


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("author", "comment", "contentType", "published", "id")

    def create(self, validated_data):
        post_id = self.context['post_id']
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(username=self.context['user'].username)
        comment = Comment.objects.create(parent_post=post, author=user, **validated_data)
        return comment


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('categories')


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

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'source', 'origin', 'description', 'author', 'categories', 'contentType', 'content',
            'published',
            'visibility', 'unlisted', 'comments')

    def create(self, validated_data):

        if 'categories' in validated_data.keys():
            categories_data = validated_data.pop('categories')
        else:
            categories_data = []

        user = User.objects.get(username=self.context['user'].username)
        post = Post.objects.create(author=user, **validated_data)

        for category_data in categories_data:
            post.categories.add(category_data)

        # apparently create calls .save() implicitly
        return post
