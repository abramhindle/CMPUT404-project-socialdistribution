from rest_framework import serializers
from presentation.models import Inbox

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = ['type', 'author', 'items']
