from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    display_name = serializers.CharField(required=False)
    github_url = serializers.URLField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'display_name', 'github_url')
        
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
