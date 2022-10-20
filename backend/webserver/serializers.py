from rest_framework import serializers
from .models import Author, FollowRequest


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['url', 'id', 'display_name', 'profile_image', 'github_handle']


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


class FollowRequestSerializer(serializers.ModelSerializer):
    sender = AuthorSerializer(read_only=True)

    class Meta:
        model = FollowRequest
        fields = ['sender']

    # reduces one layer of nesting i.e. removes the 'sender' key and just returns the value instead
    def to_representation(self, instance):
        data = super(FollowRequestSerializer, self).to_representation(instance)
        return data['sender']
