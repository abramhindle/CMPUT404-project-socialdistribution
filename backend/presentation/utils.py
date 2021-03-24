from presentation.Serializers.user_serializer import UserSerializer


def myJwtResponseHandler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
