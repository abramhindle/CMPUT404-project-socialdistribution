from rest_framework import serializers

from .models import DummyPost


class DummyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyPost
        fields = ('id', 'text', )
