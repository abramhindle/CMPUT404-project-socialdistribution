from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from service.models.author import Author
from django.contrib import auth
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import json

class SignInSerializerForm(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SignUpSerializerForm(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    displayName = serializers.CharField()
    profileImage = serializers.URLField()
    github = serializers.URLField()


@method_decorator(csrf_exempt, name='dispatch')
class SignInView(APIView):
    permission_classes = ()
    serializer_class = SignInSerializerForm
    
    def post(self, request, format=None):   
        try:
            data = json.loads(self.request.data)
        except:
            data = self.request.data
        username = data["username"]
        password =  data["password"]

        user = auth.authenticate(username=username, password=password)
        if user:
            try:
                author = Author.objects.get(username=username)
                if(not author.is_local):
                    raise Exception
                auth.login(request, user)
                return Response({"success": "User authenticated", "author": author.toJSON()}, status=200)
            except:
                return Response({"error": "Error Authenticating"}, status=401)
        
        return Response({"error": "Error Authenticating"}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class SignOutView(APIView):
    permission_classes = ()

    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': 'Loggout Out' }, status=200)
        except:
            return Response({ 'error': 'Something went wrong when logging out' }, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(APIView):
    permission_classes = ()
    serializer_class = SignUpSerializerForm
    
    def post(self, request, format=None):   
        try:
            data = json.loads(self.request.data)
        except:
            data = self.request.data

        username = data["username"]
        password =  data["password"]
        displayName = data["displayName"]
        profileImage = data["profileImage"]
        github = data["github"]
        

        if not valid_url(github):
            return Response({"error": "github field should be a url"}, status=400)
        if not valid_url(profileImage):
            return Response({"error": "profileImage field should be a url"}, status=400)


        try:
            Author.objects.create_user(username=username, password=password, displayName=displayName, profileImage=profileImage, github=github)
            return Response({"success": "Sign Up Requested!"}, status=202)
        except IntegrityError:
            return Response({"error": "Username already in use"}, status=409)
        except:
            return Response({"error": "Error Occured"}, status=400)
        
def valid_url(to_validate):
    validator = URLValidator()
    try:
        validator(to_validate)
        return True
    except ValidationError:
        return False