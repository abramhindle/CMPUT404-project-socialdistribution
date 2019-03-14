from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..models import AuthorProfile
from ..serializers import CreateUserSerializer
from django.db import transaction
from django.conf import settings


class RegistrationView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny, )
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                user_obj = User.objects.create_user(username=request.data["username"],password=request.data["password"])
                AuthorProfile.objects.create(
                    host=settings.BACKEND_URL,
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
            return Response(str("Register failed"), status.HTTP_400_BAD_REQUEST)
