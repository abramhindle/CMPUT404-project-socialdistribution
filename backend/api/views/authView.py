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
        new_data = {
            'uuid': authorSerialized['pk'],
            'id': authorSerialized['fields']['id'],
            'username': authorSerialized['fields']['username'],
            'displayName': authorSerialized['fields']['displayName'],
            'github': authorSerialized['fields']['github'],
            'profileImage': authorSerialized['fields']['profileImage'],
        }
        result.data.update({'user': new_data})
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
def SignupView(request):
    host = request.get_host()
    if request.is_secure():
        url = 'https://'
    else:
        url = 'http://'
    host = url + host + '/'
    try:  # check if host is in data
        request.data['host']
    except:  # if host is not in data, use default host
        if request.data['host'] != None:
            request.data['host'] = host
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        signupRequest = serializer.save()
        signupRequest.save()
        return Response(status=201)
    return Response(serializer.errors , status=400)
