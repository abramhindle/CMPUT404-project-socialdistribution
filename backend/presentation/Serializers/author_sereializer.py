from rest_framework import serializers
from presentation.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("__all__")

    def create(self, validated_data):
        return Author.objects.create(**validated_data)
