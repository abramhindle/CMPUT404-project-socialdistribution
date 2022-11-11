from rest_framework import serializers
from .models import Author, Follow, FollowRequest, Inbox, Post, Node


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['url', 'id', 'display_name', 'profile_image', 'github_handle']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id','author','created_at','edited_at','title','description','source','origin','unlisted','content_type','content','visibility']

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
    id = serializers.UUIDField()
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


class AcceptOrDeclineFollowRequestSerializer(serializers.Serializer):
    follow_request_sender = ActorSerializer()


class RemoveFollowerSerializer(serializers.Serializer):
    follower = ActorSerializer()


class FollowerSerializer(serializers.ModelSerializer):
    follower = AuthorSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower']

    # reduces one layer of nesting i.e. removes the 'follower' key and just returns the value instead
    def to_representation(self, instance):
        data = super(FollowerSerializer, self).to_representation(instance)
        return data['follower']


class InboxFollowRequestSerializer(FollowRequestSerializer):
    # adds the 'sender' field back into the representation
    def to_representation(self, instance):
        data = super(InboxFollowRequestSerializer, self).to_representation(instance)
        return {"sender": data}


class InboxSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    follow_request_received = InboxFollowRequestSerializer(read_only=True)

    class Meta:
        model = Inbox
        fields = ['post', 'follow_request_received']

    # https://www.django-rest-framework.org/api-guide/relations/#generic-relationships
    def to_representation(self, instance):
        data = super(InboxSerializer, self).to_representation(instance)
        type = ''
        if instance.post:
            type = 'post'
            data = data['post']
        elif instance.follow_request_received:
            type = 'follow'
            data = data['follow_request_received']
        else:
            raise Exception('Unexpected type of inbox item')
        data['type'] = type
        return data

class AddNodeSerializer(serializers.ModelSerializer):
    api_url = serializers.URLField()
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Author
        fields = ['id', 'api_url', 'password', 'password2']
        read_only_fields = ['id']

    def save(self):
        node_user = Author(
            username=self.validated_data['api_url'], 
            display_name=self.validated_data['api_url'],
            is_remote_user=True,
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        node_user.set_password(password)
        node = Node(user=node_user, api_url=self.validated_data['api_url'])
        node_user.save()
        node.save()
        return node_user

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['api_url']

class NodesListSerializer(serializers.ModelSerializer):
    node = NodeSerializer()
    class Meta:
        model = Author
        fields = ['id', 'node', 'password']
