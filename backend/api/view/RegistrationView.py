from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..models import AuthorProfile
from ..serializers import CreateUserSerializer, UserSerializer
from django.db import transaction


class RegistrationView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny, )
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                user_obj = User.objects.create_user(username=request.data["username"],password=request.data["password"])
                AuthorProfile.objects.create(
                    host="http://localhost:8000/", 
                    displayName=request.data["displayName"], 
                    github=request.data["github"], 
                    bio=request.data["bio"], 
                    user=user_obj, 
                    firstName=request.data["firstName"], 
                    lastName=request.data["lastName"], 
                    email=request.data["email"], isValid=False
                    )
                return Response("Register success", status.HTTP_200_OK)
                
        except Exception as e:
            print("error: "+str(e))
            return Response(str("Register failed"), status.HTTP_400_BAD_REQUEST)
        # user = User.objects.create_user()
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.save()
        # return Response({
        #     "user": UserSerializer(user,
        #                            context=self.get_serializer_context()).data
        # })
