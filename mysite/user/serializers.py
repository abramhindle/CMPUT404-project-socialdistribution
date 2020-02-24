from rest_framework import serializers
from .models import *
from rest_framework.pagination import PageNumberPagination

class AuthorSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return f"{obj.host}author/{obj.username}"

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','host','github','bio','url']