from django.http import response
from django.http.request import HttpRequest
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from apps.inbox.models import InboxItem
from apps.core.models import Author, Follow
from apps.core.serializers import FollowSerializer
from apps.posts.models import Comment
from apps.posts.serializers import PostSerializer, LikeSerializer, CommentSerializer
from apis.likes.views import create_like
from apis.posts.views import create_or_get_comment
from rest_framework import status
import json
from socialdistribution.utils import Utils
# Create your views here.

def post_external_inbox(author_id, data):
    Utils.postToUrl(author_id + "/inbox", data)

def create_follow(follower_id, target_id, host):
    follower_id = Utils.cleanAuthorId(follower_id, host)
    target_id = Utils.cleanAuthorId(target_id, host)
    follow = Follow.objects.create(target_id = target_id, follower_id = follower_id)
    follow.save()
    return follow

def create_inbox_item(author: dict, sender:dict, data:dict, host: str):
    if (author["host"] != host):
        post_external_inbox(author["id"], data)

    item_content = None
    item_id = None

    if data["type"] == InboxItem.ItemTypeEnum.LIKE:
        like = create_like(sender["url"], sender["displayName"], data["object"], host)
        if (like == None):
            return HttpResponseBadRequest("liked object doesn't exist")
        if (author["host"] == host):
            item_id=str(data["author"]["id"]) + ', ' + data["object"]
    elif data["type"] == InboxItem.ItemTypeEnum.FOLLOW:
        follower = create_follow(sender['url'], author["url"], host)
        if (follower == None):
            return HttpResponseBadRequest("Unable to find follower or unable to find target")
        if (author["host"] == host):
            item_id=str(data["actor"]["id"]) + ', ' + str(data["object"]["id"])
    elif (author["host"] == host):
        if (data["type"] == InboxItem.ItemTypeEnum.COMMENT):
            serializer = CommentSerializer(data=data)
            comment_id = Utils.getCommentId(data["id"])
            post_id = Utils.getPostId(data["id"])
            if (serializer.is_valid()):
                comment = create_or_get_comment(sender["id"], post_id, serializer, comment_id)
                serializer = CommentSerializer(comment, context={'host': host})
                if (comment == None):
                    return HttpResponseBadRequest("object being commented on doesn't exist")
                else:
                    data["id"] = serializer.id
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        item_id=data["id"]
    
    if (item_id != None):
        item_content = json.dumps(data, default=lambda x: x.__dict__)
        item = InboxItem.objects.create(author_id=author["id"], item_id=item_id, item_type=data["type"], item=item_content)
        item.save()
    
    return (None, item_content)

class inbox(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str):
        """
        Provides Http responses to GET requests that query these forms of URL

        127.0.0.1:8000/author/<author-id>/inbox

        Validates author-id and authenticates that this request is allowed

        If authenticated get a list of posts sent to author with author-id=<author-id>

        args:
            - request: a request to get an inbox
            - author_id: uuid of the requested author
        returns:
            - HttpResponse containing list of posts sent to author if author is validated and client has permission
            - else HttpResponseNotFound is returned

        """
        host = Utils.getRequestHost(request)
        author_id = Utils.cleanAuthorId(author_id, host)

        try:
            if (not Author.objects.get(pk=author_id)):
                raise Http404()
        except:
            raise Http404()

        items = []
        try:
            queryset = InboxItem.objects.order_by('created_at').filter(author_id=author_id)
            items = self.paginate_queryset(queryset)
        except InboxItem.DoesNotExist:
            items = []

        data = {
            "type": "inbox",
            "author": host + "/author/" + str(author_id),
        }

        parsed_items = []
        if (items and len(items) > 0):
            for item in items:
                parsed_items.append(json.loads(item.item))

        formatted_data = Utils.formatResponse(query_type="GET on index", data=parsed_items, obj_type="inbox")
        result = self.get_paginated_response(formatted_data)
        data = {**data, **result.data} 

        return JsonResponse(data, safe=False)

    def post(self, request: HttpRequest, author_id: str):
        """
        Provides Http responses to POST requests that query these forms of URL

        127.0.0.1:8000/author/<author-id>/inbox

        Validates author-id and sends a post to the author having author-id=<author-id>

        if the type is “post” then it adds that post to the author’s inbox
        if the type is “follow” then it adds that follow to the author’s inbox to approve later
        if the type is “like” then it adds that like to the author’s inbox and creates the like object
        if the type is “comment” then it adds that comment to the author’s inbox and creates the comment object

        author_id must be an author in this host, unless type is like, in which case you are allowed
        to like the comment of an external user if their comment is stored on this host. The like will
        only be created, not stored in an inbox. A call must be made to the authors inbox on the other 
        host to add the like to their inbox (and to their database so they can return the objects this user has liked)

        args:
            - request: a request to post to an inbox, add a like to an inbox, add follow to inbox
            - author_id: uuid of the requested author
        returns:
            - Response containing formatted data about post
            - HttpResponseBadRequest if type or id is not known

        """
        host = Utils.getRequestHost(request)
        author_id = Utils.cleanAuthorId(author_id, host)

        if (not request.user or request.user.is_anonymous):
            return HttpResponse('Unauthorized', status=401)

        data: dict = JSONParser().parse(request) if request.data is str else request.data
        if (not data):
            return HttpResponseBadRequest("Empty body")

        itemAuthorId = None
        if (data.__contains__("author") and data["author"].__contains__("id")):
            itemAuthorId = Utils.cleanAuthorId(data["author"]["id"], host)
        elif (data.__contains__("actor") and data["actor"].__contains__("id")):            
            itemAuthorId = Utils.cleanAuthorId(data["actor"]["id"], host)
        sender:dict = None
        if (itemAuthorId):
            sender = Utils.getAuthorDict(itemAuthorId, host, True)
        if (sender == None):
            return HttpResponseNotFound("Unable to find sender")

        currentAuthor=Author.objects.filter(userId=request.user).first()
        if (not request.user.is_staff and not currentAuthor.isServer):
            if (itemAuthorId != currentAuthor.id):
                return HttpResponseForbidden()

        if (not data.__contains__("type")):
            return HttpResponseBadRequest("Body must contain the type of the item")

        author = Utils.getAuthorDict(author_id, host, True)

        serializer = None
        if data["type"] == InboxItem.ItemTypeEnum.LIKE:
            if (itemAuthorId == None or not data.__contains__("object")):
               return HttpResponseBadRequest("Body must contain the author and the id of the object")

            serializer = LikeSerializer(data=data, context={'host': host})
        elif data["type"] == InboxItem.ItemTypeEnum.FOLLOW:
            if (itemAuthorId == None or not data.__contains__("object") or not data["object"].__contains__("id")):
               return HttpResponseBadRequest("Body must contain the actor, the object, and their ids")
            serializer = FollowSerializer(data=data, context={'host': host})
        else:
            if (not data.__contains__("id") and data["type"] != InboxItem.ItemTypeEnum.FOLLOW):
                return HttpResponseBadRequest("Body must contain the id of the item. A comment that does not exist yet must contain the id of the post being commented on.")

            if data["type"] == InboxItem.ItemTypeEnum.POST:
                serializer = PostSerializer(data=data)
            elif data["type"] == InboxItem.ItemTypeEnum.FOLLOW:
                # Followers aren't serialized so manual checks for this
                if (not data.__contains__("actor") or not data["actor"].__contains__("id") or
                    not data.__contains__("object") or not data["object"].__contains__("id")):
                    return HttpResponseBadRequest("Follow must contain the actor and object")
                if (Utils.cleanAuthorId(data["object"]["id"], host) != author_id):
                    return HttpResponseBadRequest("A follow request can only be sent to the inbox of the author being followed. The object id must match the author_id in the url.")
            else:
                return HttpResponseBadRequest(data["type"] + "Is not a known type of inbox item")

        if (serializer and not serializer.is_valid()):
            return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        existing = None

        try:
            if data["type"] == InboxItem.ItemTypeEnum.LIKE:
                existing = InboxItem.objects.get(item_id=str(data["author"]["id"]) + ', ' + data["object"], author_id=author_id)
            elif data["type"] == InboxItem.ItemTypeEnum.FOLLOW:
                existing = InboxItem.objects.get(item_id=str(data["actor"]["id"]) + ', ' + data["object"]["id"], author_id=author_id)
            else:
                existing = InboxItem.objects.get(item_id=data["id"], author_id=author_id)
        except InboxItem.DoesNotExist:
            pass
        except: # probably the json didn't even have an id field
            return HttpResponseBadRequest()

        if (existing != None):
            existing.delete()
        
        (errorResponse, item_content) = create_inbox_item(author, sender, data, host)
        if (errorResponse != None):
            return errorResponse

        formatted_data = Utils.formatResponse(query_type="POST on inbox", data=data)
        return Response(formatted_data, status=status.HTTP_201_CREATED)

    def delete(self, request: HttpRequest, author_id: str):
        """
        Provides Http responses to DELETE requests that query these forms of URL

        127.0.0.1:8000/author/<author-id>/inbox

        Clears the inbox of author having author-id=<author-id> if authenticated to do so

        args:
            - request: a request to delete posts from a certain author in inbox
            - author_id: uuid of the requested author
        returns:
            - HttpResponse if deleted posts from author_id successfully
            - Http404 otherwise
        """
        host = Utils.getRequestHost(request)
        author_id = Utils.cleanAuthorId(author_id, host)

        if (not request.user or request.user.is_anonymous):
            return HttpResponse('Unauthorized', status=401)
        
        author: Author = Utils.getAuthor(author_id)
        if (not author):
            return HttpResponseNotFound()
        
        currentAuthor=Author.objects.filter(userId=request.user).first()
        if (currentAuthor.id != author_id and not request.user.is_staff):
            return HttpResponseForbidden()

        items = InboxItem.objects.filter(author_id=author_id)

        if (items):
            for item in items:
                item.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        else:
            return HttpResponseNotFound()


# Examples of calling api
# author uuid(replace): "4f890507-ad2d-48e2-bb40-163e71114c27"
# post uuid(replace): "d57bbd0e-185c-4964-9e2e-d5bb3c02841a"
# Authentication admin(replace): "YWRtaW46YWRtaW4=" (admin:admin)

# GET
# curl 127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/inbox

# POST
# curl http://127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/inbox -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
# "type":"post",
# "title":"A Friendly post title about a post about web dev",
# "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
# "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
# "origin":"http://whereitcamefrom.com/posts/zzzzz",
# "description":"This post discusses stuff -- brief",
# "contentType":"text/plain",
# "content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
# "author":{
#       "type":"author",
#       "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
#       "host":"http://127.0.0.1:5454/",
#       "displayName":"Lara Croft",
#       "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
#       "github": "http://github.com/laracroft",
#       "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
# },
# "categories":["web","tutorial"],
# "comments":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
# "published":"2015-03-09T13:07:04+00:00",
# "visibility":"FRIENDS",
# "unlisted":false}'  

# curl http://127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/inbox -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
#     "id":"d57bbd0e-185c-4964-9e2e-d5bb3c02841a",
#     "type":"post",
#     "title":"A post posted with put api on /post/",
#     "description":"This post discusses stuff -- brief",
#     "contentType":"text/plain",
#     "author":{
#           "type":"author",
#           "id":"4f890507-ad2d-48e2-bb40-163e71114c27"
#     },
#     "visibility":"PUBLIC",
#     "unlisted":false}'    

# POST like
# curl http://localhost:8000/author/3dfa865b-5926-4c4c-b6cd-11853dcb0622/inbox -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
# "type":"like",
# "author":{
#       "type":"author", 
#       "id":"3dfa865b-5926-4c4c-b6cd-11853dcb0622"
# },
# "object":"http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/post/d57bbd0e-185c-4964-9e2e-d5bb3c02841a/comments/a44bacba-c92e-4bf3-a616-aa352cbd1cda"}'

# DELETE
# curl -X DELETE http://127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/inbox -H "Authorization: Basic YWRtaW46YWRtaW4="

# curl http://localhost:8000/author/eb085f68-6af2-4ba1-89a6-2391551b1984/inbox  -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
# "type": "like", 
# "object": "http://127.0.0.1:8000/author/eb085f68-6af2-4ba1-89a6-2391551b1984/posts/27921214-ae32-4872-8253-4d4667e91d27/comments/55c7fb30-6da1-43f3-ae60-8089470e5066", 
# "author": {
#       "type": "author", 
#       "id": "eb085f68-6af2-4ba1-89a6-2391551b1984" 
# }
# }'

# POST follow
# curl http://localhost:8000/author/3dfa865b-5926-4c4c-b6cd-11853dcb0622/inbox  -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
# "type": "follow", 
# "actor": { 
#       "type": "author", 
#       "id": "eb085f68-6af2-4ba1-89a6-2391551b1984" 
# }, 
# "object": {
#       "type": "author", 
#       "id": "3dfa865b-5926-4c4c-b6cd-11853dcb0622" 
# }
# }'

# Remote following local example
# curl http://localhost:8000/author/dd0060fa-e4ec-4e2c-aa4e-0a24f724a532/inbox  -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{"type": "follow", "actor": { "type": "author", "id": "http://127.0.0.1:8080/author/4f68a791-9526-4a13-9b9e-19e06b24f6f0" }, "object": {"type": "author", "id": "dd0060fa-e4ec-4e2c-aa4e-0a24f724a532" }}'

