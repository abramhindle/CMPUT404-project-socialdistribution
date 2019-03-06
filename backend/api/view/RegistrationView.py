from rest_framework import generics
from rest_framework.response import Response

from ..serializers import CreateUserSerializer, UserSerializer, AuthorProfileSerializer
from ..models import AuthorProfile

class RegistrationView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        author_profile = AuthorProfile.objects.create(host="http://localhost:8000/", displayName="displayName_value", user=user)
        return Response({
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data
        })
