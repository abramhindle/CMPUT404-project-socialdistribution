from re import search
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
from requests.models import HTTPBasicAuth, Response
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import Serializer
from apps.core.models import Author, ExternalHost
from apps.core.serializers import AuthorSerializer
import requests

class Utils():
    @staticmethod
    def getAcceptedMediaType(request: HttpRequest):
        if (request.headers.__contains__("Accept")):
            return request.headers["Accept"]
        else:
            return "application/json"

    @staticmethod
    def serialize(data: dict, request: HttpRequest):
        return JSONRenderer().render(data, Utils.getAcceptedMediaType(request))

    @staticmethod
    def getUrlHost(url: str):
        res = search('^(.*)://([^/]*)', url)
        if (res and len(res.group) == 3):
            scheme = res.group(1)
            host = res.group(2)
            return scheme + "://" + host
        return None

    @staticmethod
    def getRequestHost(request: HttpRequest):
        return request.scheme + "://" + request.get_host()

    @staticmethod
    def cleanId(id: str, host: str):
        id_host = Utils.getUrlHost(id)
        if (id_host and id_host == host):
            return Utils.getAuthorId(id)
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

    @staticmethod
    def getAuthor(author_id: str) -> Author:
        try:
            return Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise Http404()

    @staticmethod
    def getAuthorId(url:str):
        res = search('author(s?)/(?P<id>[^/]*)$', url)
        if (res and res.group and res.group('id')):
            return res.group('id')
        return None
    
    @staticmethod
    def getPostId(url:str):
        res = search('post(s?)/(?P<id>[^/]*)$', url)
        if (res and res.group and res.group('id')):
            return res.group('id')
        return None

    @staticmethod
    def getCommentId(url:str):
        res = search('comment(s?)/(?P<id>[^/]*)$', url)
        if (res and res.group and res.group('id')):
            return res.group('id')
        return None
    
    @staticmethod
    def getFromUrl(url:str) -> Response:
        host = Utils.getUrlHost(url)
        try:
            externalHost = ExternalHost.objects.get(host=host)
        except:
            raise Http404()

        if (externalHost):
            response = requests.get(url, auth=HTTPBasicAuth(username=externalHost.username, password=externalHost.password))
            if (response.status_code != 200):
                raise HttpResponse(response.reason, status=response.status_code)
            return response.json()
            
        raise Http404()

    # Used for formatting and styling responses
    @staticmethod
    def formatResponse(query_type, data):
        json_result = {
            'query': query_type,
            'data': data
        }

        return json_result