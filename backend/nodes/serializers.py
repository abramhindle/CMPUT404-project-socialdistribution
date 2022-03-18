from rest_framework import serializers
from .models import Node


class NodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Node
        write_only_fields = ["username", "password"]
        fields = ["name", "host", "username", "password"]
    
    def create(self, validated_data):
        validated_data.pop('username', None)
        validated_data.pop('password', None)
        return super().create(validated_data)
