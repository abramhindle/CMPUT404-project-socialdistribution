from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from service.models.author import Author
from django.contrib import auth
import json
        
class SignInSerializerForm(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignInView(APIView):
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
        

class SignOutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': 'Loggout Out' }, status=200)
        except:
            return Response({ 'error': 'Something went wrong when logging out' }, status=401)