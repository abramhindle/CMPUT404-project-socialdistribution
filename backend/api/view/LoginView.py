from rest_framework import generics, permissions,status
from rest_framework.response import Response
from ..serializers import LoginUserSerializer
from ..models import AuthorProfile
from .Util import *

class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user = serializer.validated_data
        try:
            auth_profile = AuthorProfile.objects.get(user=current_user)
            if(not auth_profile.isValid):
                httpStatus = status.HTTP_400_BAD_REQUEST
                returnError = "Error: User is not approved by admin"
                return Response(returnError, httpStatus)
        except:
            return Response("Invalid username/password entered", status.HTTP_400_BAD_REQUEST)

        # todo return profile pic when implemented
        response_data = {
            "authorId": get_author_id(auth_profile, False),
            "displayName": auth_profile.displayName
        }

        http_status = status.HTTP_200_OK
        return Response(response_data, http_status)
