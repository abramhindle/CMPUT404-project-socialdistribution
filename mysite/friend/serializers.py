from .models import Friend
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

class FriendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friend
        fields = "__all__"