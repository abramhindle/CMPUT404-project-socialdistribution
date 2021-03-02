from rest_framework import serializers
from presentation.models import Request


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['_type', 'summary', 'actor', 'object']
