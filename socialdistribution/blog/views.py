from rest_framework.views import APIView
from rest_framework.response import Response
from service.models.author import Author
from django.contrib import auth

class SignInView(APIView):
    def post(self, request, format=None):
        data = self.request.data

        username = data["username"]
        password = data["password"]

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