from rest_framework import serializers
from .models import Node


class NodeSerializer(serializers.ModelSerializer):
    remote_username = serializers.CharField(write_only=True)
    remote_password = serializers.CharField(write_only=True)

    class Meta:
        model = Node
        write_only_fields = ["username", "password"]
        fields = ["name", "host", "username", "password", "remote_username", "remote_password"]

    def create(self, validated_data):
        validated_data.pop('remote_username', None)
        validated_data.pop('remote_password', None)
        return super().create(validated_data)