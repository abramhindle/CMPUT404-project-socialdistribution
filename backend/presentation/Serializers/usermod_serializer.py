from rest_framework import serializers
from presentation.models import Usermod


class UsermodSerializer(serializers.ModelSerializer):
	class Meta:
		model = Usermod
		fields = ["allowLogin"]

