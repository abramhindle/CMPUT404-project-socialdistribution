from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from service.models.author import Author

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if Author.objects.filter(user = user).exists():
            token = super().get_token(user)
            token['username'] = user.username
            token['email'] = user.email
            return token
        else:
            return None