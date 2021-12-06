from apps.core.models import Author, Follow
from rest_framework import serializers
from re import search

def getUrlHost(url: str):
    res = search('^(.*)://([^/]*)', url)
    if (res and len(res.group) == 3):
        scheme = res.group(1)
        host = res.group(2)
        return scheme + "://" + host
    return None

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author", read_only=True)
    url = serializers.SerializerMethodField('get_url')
    host = serializers.SerializerMethodField('get_host')
    isAdmin = serializers.SerializerMethodField('get_isAdmin')

    def get_url(self, obj):
        host = self.context.get("host")
        objHost = getUrlHost(obj.id)
        if (objHost):
            return obj.id
        elif(host):
            return host + "/author/" + str(obj.id)
        
        return None


    def get_host(self, obj):
        host = self.context.get("host")
        objHost = getUrlHost(obj.id)
        if (objHost):
            return objHost
        elif (host):
            return host
        
        return None


    def get_isAdmin(self, obj):
        if (obj and obj.userId and obj.userId.is_staff):
            return True
        
        return False


    class Meta:
        model = Author
        fields = [
            'type',
            'id',
            'url',
            'host',
            'displayName',
            'github',
            'profileImage',
            'isAdmin',
            'isApproved',
            'isServer'
        ]


class FollowSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="follow", read_only=True)
    actor = AuthorSerializer(read_only=True, source='follower')
    object = AuthorSerializer(read_only=True, source='target')
    summary = serializers.CharField(read_only=True)

    class Meta:
        model = Follow
        fields = [
            'summary', 
            'type',
            'actor',
            'object',
        ]