from rest_framework import generics, permissions,status
from rest_framework.response import Response
from ..serializers import UserSerializer, LoginUserSerializer
from ..models import AuthorProfile


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user = serializer.validated_data
        try:
            auth_profile = AuthorProfile.objects.filter(user=current_user)[0]
            if(not auth_profile.isValid):
                httpStatus = status.HTTP_400_BAD_REQUEST
                returnError = "Error: User is not approved by admin"
                return Response(returnError, httpStatus)
        
        except:
            print("Invalid username/password entered")
        stringUser = auth_profile.host+"author/"+str(auth_profile.id)
        httpStatus = status.HTTP_200_OK
        return Response(stringUser, httpStatus)
