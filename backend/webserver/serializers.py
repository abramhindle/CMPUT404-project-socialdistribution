from rest_framework import serializers
from .models import Author, Follow, FollowRequest, Post


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['url', 'id', 'display_name', 'profile_image', 'github_handle']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['author','created_at','edited_at','title','description','source','origin','unlisted','content_type','content','visibility']

class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','description','unlisted','content']
    
    

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','description','unlisted','content','visibility',"content_type"]


class AuthorRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Author
        fields = ['username', 'display_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        author = Author(username=self.validated_data['username'], display_name=self.validated_data['display_name'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        author.set_password(password)
        author.save()
        return author


class ActorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    url = serializers.URLField()


class SendFollowRequestSerializer(serializers.Serializer):
    sender = ActorSerializer()
    receiver = ActorSerializer()
    
class SendPrivatePostSerializer(serializers.Serializer):
    receiver = ActorSerializer()

class FollowRequestSerializer(serializers.ModelSerializer):
    sender = AuthorSerializer(read_only=True)

    class Meta:
        model = FollowRequest
        fields = ['sender']

    # reduces one layer of nesting i.e. removes the 'sender' key and just returns the value instead
    def to_representation(self, instance):
        data = super(FollowRequestSerializer, self).to_representation(instance)
        return data['sender']


class AcceptFollowRequestSerializer(serializers.Serializer):
    follow_request_sender = ActorSerializer()

class FollowerSerializer(serializers.ModelSerializer):
    follower = AuthorSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower']

    # reduces one layer of nesting i.e. removes the 'follower' key and just returns the value instead
    def to_representation(self, instance):
        data = super(FollowerSerializer, self).to_representation(instance)
        return data['follower']
