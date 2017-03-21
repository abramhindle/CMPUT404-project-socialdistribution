from rest_framework import serializers

from social.app.models.author import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('user', 'id', 'displayName', 'github', 'bio', 'activated', 'node',)


