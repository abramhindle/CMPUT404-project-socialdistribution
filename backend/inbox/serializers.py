from rest_framework import serializers
from .models import InboxItem


class InboxItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InboxItem
        fields = ["id", "owner", "src"]
