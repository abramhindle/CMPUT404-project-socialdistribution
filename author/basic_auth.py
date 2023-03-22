from django.contrib.auth import authenticate
from django.http import HttpResponse
import base64

class BasicAuthenticator:
    
    def check(self, request, *args, **kwargs):
        authentication_header = request.META.get('HTTP_AUTHORIZATION')
        if not authentication_header:
            result = HttpResponse('Authentication Required', status=401)
            result['WWW-Authenticate'] = 'Basic realm="API"'
            return result

        authentication, user_pass = authentication_header.split(' ', 1)

        if authentication.lower != 'basic':
            result = HttpResponse('Authentication Required', status=401)
            result['WWW-Authenticate'] = 'Basic realm="API"'
            return result

        user_pass_split = base64.b64decode(user_pass.encode('utf-8')).decode('utf-8').split(':')
        
        username = user_pass_split[0]
        password = user_pass_split[1]

        node = authenticate(request, username=username, password=password)

        if not node:
            result= HttpResponse('Authentication Required', status=401)
            result['WWW-Authenticate'] = 'Basic realm="API"'
            return result
        
        request.node = node
        return super().dispatch(request, *args, **kwargs) 

    