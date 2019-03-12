from rest_framework import generics, permissions,status
from rest_framework.response import Response
from ..serializers import LoginUserSerializer
from ..models import AuthorProfile


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        print(request, "adgadfadfasfd")
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

        stringUser = auth_profile.host+"author/"+str(auth_profile.id)
        httpStatus = status.HTTP_200_OK
        return Response(stringUser, httpStatus)
