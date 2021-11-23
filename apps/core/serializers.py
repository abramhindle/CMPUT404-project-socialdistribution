from apps.core.models import Author
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author", read_only=True)
    url = serializers.SerializerMethodField('get_url')
    host = serializers.SerializerMethodField('get_host')

    def get_url(self, obj):
        host = self.context.get("host")
        if (host):
            return host + "/author/" + str(obj.id)
        
        return None


    def get_host(self, obj):
        host = self.context.get("host")
        if (host):
            return host
        
        return None


    class Meta:
        model = Author
        fields = [
            'type',
            'id',
            'url',
            'host',
            'displayName',
            'github',
            'profileImage'
        ]