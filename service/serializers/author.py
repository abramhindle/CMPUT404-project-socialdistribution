from rest_framework import serializers
from service.models.author import Author

class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField("set_id")

    def set_id(self, author):
        return str(author._id)

    class Meta:
        model = Author
        fields = ("type", "id", "host", "displayName", "url", "github", "profileImage")