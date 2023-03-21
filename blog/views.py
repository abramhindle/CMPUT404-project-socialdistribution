from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from service.models.author import Author
from django.contrib import auth
from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

class SignInSerializerForm(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

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
        if user is not None:
            try:
                author = Author.objects.get(user=user)
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