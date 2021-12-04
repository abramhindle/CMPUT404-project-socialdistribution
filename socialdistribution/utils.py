from re import search
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
from requests.models import HTTPBasicAuth, Response
from rest_framework.renderers import JSONRenderer
from apps.core.models import Author, ExternalHost
from apps.posts.models import Comment
from apps.posts.serializers import CommentSerializer
from apps.core.serializers import AuthorSerializer
import requests
from base64 import b64encode

class Utils():
    @staticmethod
    def getAcceptedMediaType(request: HttpRequest):
        if (request.headers.__contains__("Accept")):
            return request.headers["Accept"]
        else:
            return "application/json"

    @staticmethod
    def serialize(data: dict, request: HttpRequest):
        media = Utils.getAcceptedMediaType(request)
        return JSONRenderer().render(data, media)

    @staticmethod
    def getUrlHost(url: str):
        res = search('^(?P<scheme>.*)://(?P<host>[^/]*)', url)
        if (res and res.group and res.group('scheme') and res.group('host')):
            scheme = res.group('scheme')
            host = res.group('host')
            res2 = search('^127.0.0.1:(?P<port>.*)', host)
            if (res2 and res2.group and res2.group('port')):
                host = "localhost:" + res2.group('port')
            return scheme + "://" + host
        return None

    @staticmethod
    def getRequestHost(request: HttpRequest):
        return request.scheme + "://" + request.get_host()

    @staticmethod
    def areSameHost(host1, host2):
        res = search('^(?P<scheme>.*)://127.0.0.1:(?P<port>[^/]*)', host1)
        if (res and res.group and res.group('scheme') and res.group('port')):
            host1 = res.group('scheme') + "://localhost:" + res.group('port')
        res2 = search('^(?P<scheme>.*)://127.0.0.1:(?P<port>[^/]*)', host2)
        if (res2 and res2.group and res2.group('scheme') and res2.group('port')):
            host2 = res2.group('scheme') + "://localhost:" + res2.group('port')
        return host1 == host2

    @staticmethod
    def cleanAuthorId(id: str, host: str):
        id_host = Utils.getUrlHost(id)
        if (id_host and Utils.areSameHost(id_host, host)):
            return Utils.getAuthorId(id)
        return id

    @staticmethod
    def cleanCommentId(id: str, host: str):
        id_host = Utils.getUrlHost(id)
        if (id_host and Utils.areSameHost(id_host, host)):
            return Utils.getCommentId(id)
        return id

    @staticmethod
    def cleanPostId(id: str, host: str):
        id_host = Utils.getUrlHost(id)
        if (id_host and Utils.areSameHost(id_host, host)):
            return Utils.getPostId(id)
        return id
    
    # Helper function with error checking to get Author object from id
    @staticmethod
    def getAuthorDict(author_id: str, host:str, allowExternal: bool = True) -> dict:
        try:
            author = Author.objects.get(pk=author_id)
            if (author):
                serializer = AuthorSerializer(author, context={'host': host})
                return serializer.data
        except Author.DoesNotExist:
            if (allowExternal):
                return Utils.getFromUrl(author_id)
        raise Http404()

    # Helper function with error checking to get Author object from id
    @staticmethod
    def getCommentDict(comment_id: str, host:str, allowExternal: bool = True) -> dict:
        id_host = Utils.getUrlHost(comment_id)
        if (id_host and id_host != host and allowExternal):
            return Utils.getFromUrl(comment_id)

        try:
            comment = Comment.objects.get(pk=comment_id)
            if (comment):
                serializer = CommentSerializer(comment, context={'host': host})
                return serializer.data
        except Author.DoesNotExist:
            raise Http404()
        raise Http404()

    @staticmethod
    def getAuthor(author_id: str) -> Author:
        try:
            return Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise Http404()

    @staticmethod
    def getAuthorId(url:str):
        """ 
        Returns an id of a proper athor entity, None otherwise
        """
        res = search('author(s?)/(?P<id>[^/]*)(/)?$', url)
        if (res and res.group and res.group('id')):
            return res.group('id')
        return None
    
    @staticmethod
    def getPostId(url:str):
        """ 
        Returns an id of a proper post entity, None otherwise
        """
        res = search('post(s?)/(?P<id>[^/]*)(/)?$', url)
        if (res and res.group and res.group('id')):
            return res.group('id')
        return None

    @staticmethod
    def getCommentId(url:str):
        """ 
        Returns an id of a proper comment entity, None otherwise
        """
        res = search('comment(s?)/(?P<id>[^/]*)(/)?$', url)
        if (res and res.group and res.group('id')):
            return res.group('id')
        return None

    @staticmethod
    def extractPostId(url:str):
        """ 
        Returns an id of a post from any uri matching syntax "posts?/id(/any)?", None otherwise
        """
        res = search('post(s?)/(?P<id>[^/]*)(/.*)?$', url)
        if (res and res.group and res.group('id')):
            return res.group('id')
        return None
    
    @staticmethod
    def getFromUrl(url:str) -> Response:
        host = Utils.getUrlHost(url)
        try:
            externalHost = ExternalHost.objects.get(host__startswith=host)
        except:
            raise Http404()
        
        response = None
        if (externalHost):
            if externalHost.username and externalHost.password:
                response = requests.get(url, auth=HTTPBasicAuth(username=externalHost.username, password=externalHost.password))
            elif externalHost.token:
                headers = { 'Authorization' : 'Basic %s' %  externalHost.token }
                response = requests.get(url, headers=headers)
            else:
                response = requests.get(url)

            if (response.status_code != 200):
                raise Http404()
            return response.json()
            
        raise Http404()
    
    
    @staticmethod
    def postToUrl(url:str, data) -> Response:
        host = Utils.getUrlHost(url)
        try:
            externalHost = ExternalHost.objects.get(host__startswith=host)
        except:
            raise Http404()
        
        response = None
        if (externalHost):
            if externalHost.username and externalHost.password:
                response = requests.post(url, data=data, auth=HTTPBasicAuth(username=externalHost.username, password=externalHost.password))
            elif externalHost.token:
                headers = { 'Authorization' : 'Basic %s' %  externalHost.token }
                response = requests.post(url, data=data, headers=headers)
            else:
                response = requests.post(url, data=data)

            if (response.status_code != 200):
                raise Http404()
            return response.json()
            
        raise Http404()

    # Used for formatting and styling responses
    @staticmethod
    def formatResponse(query_type, data, obj_type=None):
        if obj_type is not None:
            json_result = {
                'query': query_type,
                'type': obj_type,
                'data': data
            }
        else:
            json_result = {
                'query': query_type,
                'data': data
            }
            

        return json_result