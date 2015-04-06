import base64

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from author.models import Author
from socialdistribution.settings import LOCAL_HOST, ALLOWED_HOSTS

'''sample curl:
curl -v -u "mel:social-distribution.herokuapp.com:team6" social-distribution.herokuapp.com/api/author/posts'''

class AuthenticateCheck:
    def process_request(self, request, realm=" "):
        """
        This is a helper function used by 'basicauth' that determines if
        they have provided proper http-authorization. It
        returns the json requested, otherwise responding with a 401.
        """
        if not request.path.startswith('/api'):
            return

        while 1:
            if 'HTTP_AUTHORIZATION' in request.META:
                auth = request.META['HTTP_AUTHORIZATION'].split()
                if len(auth) == 2:
                    # NOTE: We are only support basic authentication for now.
                    if auth[0].lower() == "basic":
                        try:
                            user, host, password = base64.b64decode(auth[1]).split(':')
                        except:
                            break

                    if password != "team6":
                        break

                    #authenticate the host #TODO changed this to node.object
                    if host not in ALLOWED_HOSTS:
                        break

                    # local users
                    if host == LOCAL_HOST:
                        if len(User.objects.filter(username=user)) > 0:
                            request.user = User.objects.get(username=user)
                        else:
                            #correct username unnecessarily for friends API
                            return HttpResponse(status=403)
                    else:
                        #remote users
                        #make a new account, else authenticate the user
                        if('thought-bubble' in host):
                            user = 'thoughtbubble__' + user
                        elif('hindlebook' in host):
                            user = 'hindlebook__'+ user
                        else:
                            user = "__"+user
                        if len(User.objects.filter(username=user)) > 0:
                            user = User.objects.get(username=user)
                            request.user = authenticate(username=user, password=password)
                        else:
                            user = User.objects.create_user(username=user,
                                                            password=password)
                            Author.objects.create(user=user, host=host)
                            request.user = authenticate(username=user, password=password)
                    return
                else:
                    break
            else:
                break

        # Either they did not provide an authorization header or
        # something in the authorization attempt failed. Send a 401
        # back to them to ask them to authenticate.
        #

        # testing purposes
        '''response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
        return response'''

        return HttpResponse('{"message": "Authentication Failed"}', \
                            content_type='application/json', status=401)

