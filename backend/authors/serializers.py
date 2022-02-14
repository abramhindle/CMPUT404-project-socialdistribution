from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='author')
    url = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ["type", "id", "url", "host", "displayName", "github", "profileImage"]

    def get_url(self, obj: Author):
        return obj.id
        
class LoginSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = Author
        ref_name = 'LogIn'
        fields = ['displayName','password']