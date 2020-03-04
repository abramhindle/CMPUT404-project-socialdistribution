from .models import Friend
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

class FriendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friend
        fields = "__all__"
        read_only_fields = [
            "f1Id",
        ]

    def validate(self, attrs):
        f1Id = attrs.get('f1Id')
        f2Id = attrs.get('f2Id')

        if f1Id == f2Id:
            msg = _("You cannot make friend request between two same user")
            raise exceptions.ValidationError(msg)

        return attrs

        