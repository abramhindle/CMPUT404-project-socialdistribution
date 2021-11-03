from ..serializers import MyTokenObtainPairSerializer
from ..serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from ..models.authorModel import Author
from django.core import serializers
from django.http import JsonResponse
import json

# Auth Login 
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getAuthor(request):
    return authServices.currentAuthor(request)

# Login View
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request):
        result = super().post(request)
        author = Author.objects.get(username=request.data['username'])
        authorSerialized = json.loads(serializers.serialize('json', [author]))[0]
        result.data.update({'user': authorSerialized})
        result.data['token'] = result.data.pop('access')
        return result

# Obtains the currentUser token
class authServices():
    @staticmethod
    def currentAuthor(request):
        authorSerialized = json.loads(serializers.serialize('json', [request.user]))[0]
        return JsonResponse(authorSerialized)


@api_view(['POST'])
@permission_classes((AllowAny,))
def createSignupRequest(request):
    host = request.get_host()
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'
    host = protocol + host + '/'
    request.data['host'] = host
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        new_signupRequest = serializer.save()
        new_signupRequest.save()
        # to be added: redirect to some success info page
        return Response(status=201)

    print("\n\n",serializer.errors,"\n\n")
    return Response(serializer.errors , status=400)

class SignupView():
    @staticmethod
    def createSignup(request):
        return SignupView(request)