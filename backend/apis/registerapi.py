from ..models import Author
from ..serializers import AuthorSerializer, RegisterSerializer

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, status


class RegisterAPI(generics.GenericAPIView):
    """
    This class provides an API for user and author registration.
    """

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        This method provides POST functionality to creating a user and author, by serializing a user object that is created into the Django authentication system, then creating a POST request with the author data.
        """
        # Get and serialize the request data
        serializer = self.get_serializer(data=request.data)

        # Check the validity
        serializer.is_valid(raise_exception=True)

        # Create the user
        user = serializer.save()
        # Create an authentication token for the provided user
        token = Token.objects.create(user=user)

        # Create the author object
        author = Author(
            token=token,
            user=user,
            displayName=request.data["displayName"],
            github=request.data["github"],
            host=request.META['HTTP_HOST'],
        )

        # Save the author information into the database
        author.url = "http://"+str(author.host)+"/author/"+str(author.id)
        author.save()
        # Serialize the author data for a POST response
        authorData = AuthorSerializer(
            author, context=self.get_serializer_context()).data

        return Response(authorData, status=status.HTTP_201_CREATED)
