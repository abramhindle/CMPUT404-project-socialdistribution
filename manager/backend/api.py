from backend.models import Author
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import AuthorSerializer, RegisterSerializer, UserSerializer

# Get Author API
class AuthorViewSet(viewsets.ModelViewSet):
    
    queryset = Author.objects.all()

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AuthorSerializer

    lookup_field = 'id'

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context).data,
            'token': token   # creates unique token for this author
        })

# Login API