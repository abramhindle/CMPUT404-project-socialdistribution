from ..models.nodeModel import Node
from ..models.authorModel import Author
from ..serializers import AuthorSerializer
from django.http import HttpResponse
from rest_framework import authentication, exceptions, status
from rest_framework.response import Response
from urllib.parse import urlparse
import os, requests, uuid, base64

class nodeServices():
    ## Authentication of remote node(hosts) ##
    @staticmethod
    def nodeHeaders(id, userStatus=False):
        headers = {}
        ## Request header indicating the origin of the request ##
        headers['Origin'] = os.environ.get('HEROKU_HOST')
        if not userStatus:
            try:    
                author = Author.objects.get(uuid=id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializers = AuthorSerializer(author)
            headers['X-Request-User'] = serializers.data['url']
        return headers

    ## GET Request of authenticated remote node(hosts) ##
    @staticmethod
    def authenticatedNode_GET(url, node, headers=None):
        getResult = requests.get(url, auth=(node.displayName, node.password), headers=headers)
        return getResult 

    ## POST Request of authenticated remote node(hosts) ##
    @staticmethod
    def authenticatedNode_POST(url, node, body, headers=None, JSONFormat=False):
        if body!=None:
            if JSONFormat:
                postResult = requests.post(url, json=body, auth=(node.displayName, node.password), headers=headers)
            else:
                postResult = requests.post(url, data=body, auth=(node.displayName, node.password), headers=headers)
        else:
            postResult = requests.post(url, auth=(node.displayName, node.password), headers=headers)
        return postResult 

    ## PUT Request of authenticated remote node(hosts) ##
    @staticmethod
    def authenticatedNode_PUT(url, node, body, headers=None, JSONFormat=False):
        if body!=None:
            if JSONFormat:
                putResult = requests.put(url, json=body, auth=(node.displayName, node.password), headers=headers)
            else:
                putResult = requests.put(url, data=body, auth=(node.displayName, node.password), headers=headers)
        else:            
            putResult = requests.put(url, auth=(node.displayName, node.password), headers=headers)
        return putResult 

    ## DELETE Request of authenticated remote node(hosts) ##
    @staticmethod
    def authenticatedNode_DELETE(url, node, body, headers=None, JSONFormat=False):
        if body!=None:
            if JSONFormat:
                deleteResult = requests.delete(url, json=body, auth=(node.displayName, node.password), headers=headers)
            else:
                deleteResult = requests.delete(url, data=body, auth=(node.displayName, node.password), headers=headers)
        else:            
            deleteResult = requests.delete(url, auth=(node.displayName, node.password), headers=headers)
        return deleteResult 



    ## ''PUT'' Add Friend Request on remote node(hosts) ##
    @staticmethod
    def remoteAdd_Friend(request, **kwargs):
        ## Setting up the headers and the post request ##
        headers = nodeServices.nodeHeaders(request)
        urlParsed = urlparse(request.headers.get('X-Url'))
        ## scheme: The protocol name, usually http/https ;  netloc: Contains the network location ##
        parsedResult = urlParsed.scheme + "://" + urlParsed.netloc
        ## Get the established node object ##
        node = Node.objects.get(host=parsedResult)
        if not node:
            return Response("Remote connection(Node) hasn't been established", status=status.HTTP_400_BAD_REQUEST)
        else:
            url = f"{node.host}{urlParsed.path}"
            # PUT Request 
            addFriend = nodeServices.authenticatedNode_PUT(url, node, None, headers)
            return Response(addFriend.json(), status=addFriend.status_code)

    ## ''DELETE'' Add Friend Request on remote node(hosts) ##
    @staticmethod
    def remoteDelete_Friend(request, **kwargs):
        ## Setting up the headers and the post request ##
        headers = nodeServices.nodeHeaders(request)
        urlParsed = urlparse(request.headers.get('X-Url'))
        ## scheme: The protocol name, usually http/https ;  netloc: Contains the network location ##
        parsedResult = urlParsed.scheme + "://" + urlParsed.netloc
        ## Get the established node object ##
        node = Node.objects.get(host=parsedResult)
        if not node:
            return Response("Remote connection(Node) hasn't been established", status=status.HTTP_400_BAD_REQUEST)
        else:
            url = f"{node.host}{urlParsed.path}"
            # DELETE Request 
            deleteFriend = nodeServices.authenticatedNode_DELETE(url, node, request.data, headers)
            return Response(deleteFriend.text, status=deleteFriend.status_code)




    ## ''POST'' Like Requests on remote node(hosts) ##
    @staticmethod 
    def retmotePost_Like(request, **kwargs):
        ## Identifying the original host requested by the client in the Host HTTP request header ##
        hostHeader_Request = request.headers.get('X-Request-Host')
        ## Get the established node object ##
        node = Node.objects.get(host=hostHeader_Request)
        if not node:
            return Response("Remote connection(Node) hasn't been established", status=status.HTTP_400_BAD_REQUEST)
        else:
            ## Setting up the headers and the post request ##
            headers = nodeServices.nodeHeaders(request)
            urlParsed = urlparse(request.headers.get('X-Url'))
            url=f"{node.host}{urlParsed.path}"
            nodeServices.authenticatedNode_POST(url, node, request.data, headers=headers, JSONFormat=True)

    
    ## ''POST'' Comment Requests on remote node(hosts) ##
    @staticmethod
    def retmotePost_Comment(request, **kwargs):
        ## Identifying the original host requested by the client in the Host HTTP request header ##
        hostHeader_Request = request.headers.get('X-Request-Host')
        ## Get the established node object ##
        node = Node.objects.get(host=hostHeader_Request)
        if not node:
            return Response("Remote connection(Node) hasn't been established", status=status.HTTP_400_BAD_REQUEST)
        else:
            ## Setting up the headers and the post request ##
            headers = nodeServices.nodeHeaders(request)
            urlParsed = urlparse(request.headers.get('X-Url'))
            url =f"{node.host}{urlParsed.path}"
            return(nodeServices.authenticatedNode_POST(url, node, request.data, headers=headers, JSONFormat=True).json())



    ## ''POST'' Inbox Requests on remote node(hosts) ##
    def remotePost_Inbox(request, **kwargs):
        ## Identifying the original host requested by the client in the Host HTTP request header ##
        hostHeader_Request = request.headers.get('X-Request-Host')
        ## Get the established node object ##
        node = Node.objects.get(host=hostHeader_Request)
        if not node:
            return Response("Remote connection(Node) hasn't been established", status=status.HTTP_400_BAD_REQUEST)
        else:
            ## Setting up the headers and the post request ##
            headers = nodeServices.nodeHeaders(request)
            urlParsed = urlparse(request.headers.get('X-Url'))
            url=f"{node.host}{urlParsed.path}"
            return (nodeServices.authenticatedNode_POST(url, node, request.data, headers=headers, JSONFormat=True).json())
    

    ## ''POST'' Friend Request on remote node(hosts) ##
    @staticmethod
    def retmotePost_FriendRequest(request, **kwargs):
        ## Setting up the headers and the post request ##
        headers = nodeServices.nodeHeaders(request)
        urlParsed = urlparse(request.headers.get('X-Url'))
        ## scheme: The protocol name, usually http/https ;  netloc: Contains the network location ##
        parsedResult= urlParsed.scheme + "://" + urlParsed.netloc
        ## Get the established node object ##
        node = Node.objects.get(host=parsedResult)
        if not node:
            return Response("Remote connection(Node) hasn't been established", status=status.HTTP_400_BAD_REQUEST)
        else:
            url = f"{node.host}{urlParsed.path}"
            friendRequest = nodeServices.authenticatedNode_POST(url, node, request.data, headers=headers, JSONFormat=True)
            return Response(friendRequest.json(), status=friendRequest.status_code)



