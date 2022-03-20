from rest_framework import serializers
from .models import Notification
from authors.serializers import AuthorSerializer


class NotificationSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "type", "author", "actor", "summary", "published"]
