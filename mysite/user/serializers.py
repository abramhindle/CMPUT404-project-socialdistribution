from rest_framework import serializers
from .models import *
from rest_framework.pagination import PageNumberPagination

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'