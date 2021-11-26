from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.core.serializers import AuthorSerializer
from apps.core.models import Author, Follow
from rest_framework.parsers import JSONParser
from socialdistribution.utils import Utils

class author(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str) -> HttpResponse:
        """
        Provides Http responses to GET requests that query these forms of URL

        127.0.0.1:8000/author/<author-id>

        Validates author-id
        Retrieve profile if it exists, return 404 otherwise

        args:
            - request: a request to get an Author
            - author_id: uuid of the requested author
        returns:
            - HtppResponse containing author data in JSON format if found
            - else HttpResponseNotFound is returned

        """
        host = Utils.getRequestHost(request)
        author_id = Utils.cleanAuthorId(author_id, host)
        author: dict = Utils.getAuthorDict(author_id, host)
        if (author):
            return HttpResponse(Utils.serialize(author, request))
        else:
            return HttpResponseNotFound()

    def post(self, request: HttpRequest, author_id: str):
        """
        Provides Http responses to POST requests that query these forms of URL
        127.0.0.1:8000/author/<author-id>

        Validates author-id
        Update profile if it exists and has permissions, provide 404 otherwise

        args:
            - request: a request to update an Author
            - author_id: uuid of the requested author
        returns:
            - HtppResponse containing the updated author data in JSON format if found and have permissions
            - if not permissions and author found HttpBadRequest is returned
            - else return HttpResponseNotFound
        """
        if (not request.user or request.user.is_anonymous):
            return HttpResponse('Unauthorized', status=401)
        
        host = Utils.getRequestHost(request)
        author_id = Utils.cleanAuthorId(author_id, host)

        author: Author = Utils.getAuthor(author_id)
        currentAuthor=Author.objects.filter(userId=request.user).first()

        if (author):
            if ((not request.user.is_staff) and (currentAuthor.id != author.id or not author.isApproved)):
                return HttpResponseForbidden("You are not allowed to edit this author")
            
            data = JSONParser().parse(request) if request.data is str else request.data
            serializer = AuthorSerializer(data=data)

            if (serializer.is_valid()):
                if (data.__contains__("host") and data['host'] != host):
                    return HttpResponseBadRequest("The author is not from a supported host.")

                if (not data.__contains__("id") or data['id'] != str(author.id)):
                    return HttpResponseBadRequest(
                        "The id of the author in the body does not match the author_id in the request.")

                if (data.__contains__("type") and data['type'] != "author"):
                    return HttpResponseBadRequest("Can not change the type of an author")

                if (data.__contains__("displayName") and data['displayName'] != author.displayName):
                    author.displayName = data['displayName']

                if (data.__contains__("isApproved") and data['isApproved'] != author.isApproved):
                    author.isApproved = data['isApproved']

                author.github = data['github']
                author.profileImage = data['profileImage']
                author.save()

                return HttpResponse(Utils.serialize(AuthorSerializer(author, context={'host': host}).data, request))
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseNotFound()

class authors(GenericAPIView):
    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Provides Http responses to GET requests that query these forms of URL
        127.0.0.1:8000/authors

        Retrieve all profiles on the server paginated

        args:
            - request: a request to get all authors
        returns:
            - JsonResponse containing data of all authors paginated

        """
        host = Utils.getRequestHost(request)
        authors = self.filter_queryset(Author.objects.order_by('displayName').all())
        one_page_of_data = self.paginate_queryset(authors)
        serializer = AuthorSerializer(one_page_of_data, context={'host': host}, many=True)
        dict_data = Utils.formatResponse(query_type="GET on authors", data=serializer.data, obj_type="authors")
        result = self.get_paginated_response(dict_data)
        return JsonResponse(result.data, safe=False)

def create_follow(follower_id, target_id, host):
    author: dict = Utils.getAuthorDict(target_id, host)
    if not author:
        return None

    follower = Utils.getAuthorDict(follower_id, host)
    if not follower:
        return None
    
    follow = Follow.objects.create(target_id = target_id, follower_id = follower_id)
    follow.save()
    return follow

# GET all authors
# curl 127.0.0.1:8000/authors

# GET a single author
# curl 127.0.0.1:8000/author/<author_id>
# curl 127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27

# POST to update a single author. Get "yourtoken" from storage in your browser after loging in. Note the single quotes around data
# curl -d 'yourdata' 127.0.0.1:8000/author/<author_id> -H "X-CSRFToken: yourtoken" -H "Cookie: csrftoken=yourtoken" 
# curl -d '{"type": "author", "id": "a1fcf249-528a-4e8a-912c-eef7a4470696", "displayName": "Author","github": "","profileImage": ""}' 127.0.0.1:8000/author/a1fcf249-528a-4e8a-912c-eef7a4470696 -H "X-CSRFToken: DvubOcnWbnd5jfQpDGzQYGDMsz7RLIu345gPWbv01G9IQSBIOSlNuKWx1Z4ognlT" -H "Cookie: csrftoken=DvubOcnWbnd5jfQpDGzQYGDMsz7RLIu345gPWbv01G9IQSBIOSlNuKWx1Z4ognlT" 

class FollowerDetails(GenericAPIView):
    # Helper function with error checking to get follower (Author) object from follower id
    def getFollower(self, author_id: str, follower_id: str, host:str, follow: Follow = None) -> dict:
        if (follow == None):
            follow = self.getFollow(author_id, follower_id)

        try:
            serializer = AuthorSerializer(follow.follower, context={'host': host})
            return serializer.data
        except Author.DoesNotExist:
            return Utils.getFromUrl(follower_id)
        except: #above except won't work if follow if getFollow returns None
            raise Http404 

    def getFollow(self, author_id: str, follower_id: str) -> Follow:                
        try:
            return Follow.objects.get(follower_id=follower_id, target_id = author_id)
        except Exception as e:
            return None

    def getFollowers(self, author_id: str, host:str):
        allFollow = self.filter_queryset(Follow.objects.filter(target_id=author_id).order_by('follower_id'))
        one_page_of_data = self.paginate_queryset(allFollow)
        followers = []
        for follow in one_page_of_data:
            try:
                serializer = AuthorSerializer(follow.follower, context={'host': host})
                followers.append(serializer.data)
            except Author.DoesNotExist:
                try:
                    response = Utils.getFromUrl(follow.follower_id)
                    if (response):
                        followers.add(response)
                except:
                    pass
        return followers
    
    def get(self, request: HttpRequest, author_id: str, foreign_author_id: str = None):
        """
        Provides Http responses to GET requests that query these forms of URL
        1: 127.0.0.1:8000/author/<author-id>/followers
        and
        2: 127.0.0.1:8000/author/<author-id>/followers/<foreign-author-id>

        Validates author-id and (optionally) foreign-author-id

        Situation 1 will return a list of authors who follow the author with id author-id

        Situation 2 will return if a follower with id foreign-author-id follows an author with id
        author-id

        args:
            - request: a request to check if an Author has a follower or to get aall author followers
            - author_id: uuid of the requested author
            - foreign_author_id (optional): uuid of the potential follower
        returns:
            - HttpResponse if valid foreign_author_id is used containing follower data
            - HttpResponseNotFound if not a valid author or follower is not a valid author
            - JsonResponse if no foreign_author_id is provided containing list of all authors following user
        """
        host = Utils.getRequestHost(request)
        author_id = Utils.cleanAuthorId(author_id, host)

        author: dict = Utils.getAuthorDict(author_id, host)
        if not author:
            return HttpResponseNotFound("Database could not find author")
            
        if foreign_author_id:
            foreign_author_id = Utils.cleanAuthorId(foreign_author_id, host)
            follower: dict = self.getFollower(author_id, foreign_author_id, host)

            if not follower:
                return HttpResponse("%s does not follow the author or does not exist" % (foreign_author_id))

            return HttpResponse(Utils.serialize(follower, request))

        followers = self.getFollowers(author_id, host)
        dict_data = Utils.formatResponse(query_type="GET on authors", data=followers, obj_type="followers")
        result = self.get_paginated_response(dict_data).data
        return JsonResponse(result, safe=False)

    def delete(self, request: HttpRequest, author_id: str, foreign_author_id: str):
        """
        Provides Http responses to DELETE requests that query this form of URL

        127.0.0.1:8000/author/<author-id>/followers/<foreign-author-id>

        Validates author-id and foreign-author-id

        Returns a confirmation that author with author id of foreign_author_id unfollowed
        author with author id of author_id

        args:
            - request: a request to update an Author
            - author_id: uuid of the requested author
            - foreign_author_id (optional): uuid of the follower to be removed
        returns:
            - HttpNotFound if either author is not found in database
            - Response if follower was removed from author

        """
        if (not request.user or request.user.is_anonymous):
            return HttpResponse('Unauthorized', status=401)

        host = Utils.getRequestHost(request)
        author_id = Utils.cleanAuthorId(author_id, host)
        foreign_author_id = Utils.cleanAuthorId(foreign_author_id, host)

        author: dict = Utils.getAuthorDict(author_id, host)
        if not author:
            return HttpResponseNotFound("Could not find author")
        
        follow = self.getFollow(author_id, foreign_author_id)
        if not follow:
            return HttpResponseNotFound("Could not find follow object")

        currentAuthor=Author.objects.filter(userId=request.user).first()
        if (not request.user.is_staff and not currentAuthor.isServer):
            if (currentAuthor.id != foreign_author_id and currentAuthor.id != author_id):
                return HttpResponseForbidden("You are not allowed to delete this follower from this author")
        
        follow.delete()
        return Response({"detail": "id {} successfully removed".format(foreign_author_id)}, status=200)

    def put(self, request: HttpRequest, author_id: str, foreign_author_id: str):
        """
        Provides Http responses to PUT requests that query this form of URL

        127.0.0.1:8000/author/<author-id>/followers/<foreign-author-id>

        Validates author-id and (optionally) foreign-author-id

        Returns a confirmation that author with author id of foreign_author_id followed
        author with author id of author_id

        args:
            - request: a request to update an Author
            - author_id: uuid of the requested author
            - foreign_author_id (optional): uuid of the potential follower
        returns:
            - HttpResponseNotFound if not a valid author or follower is not a valid author
            - Response if follower successfully added to author
        """
        if (not request.user or request.user.is_anonymous):
            return HttpResponse('Unauthorized', status=401)
            
        host = Utils.getRequestHost(request)
        target_id = Utils.cleanAuthorId(author_id, host)
        follower_id = Utils.cleanAuthorId(foreign_author_id, host)

        follow = create_follow(follower_id, target_id, host)
        if follow == None:
            return HttpResponseNotFound("Unable to find follower or unable to find target")
        
        return Response({"detail": "id {} successfully added".format(follower_id)}, status=200)

# GET follower (get list of followers)
# curl 127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/followers

# GET follower (check if other author is a follower)
# curl 127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/followers/9f48208f-372a-45e6-a024-2b9750c9b494

# PUT follower (Follow)
# curl -X PUT 127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/followers/9f48208f-372a-45e6-a024-2b9750c9b494

# DELETE follower (Unfollow)
# curl -X DELETE 127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/followers/9f48208f-372a-45e6-a024-2b9750c9b494
