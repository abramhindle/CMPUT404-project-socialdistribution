from functools import _make_key
from django.http import response
from django.http.request import HttpRequest
from django.views import View
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.inbox.models import InboxItem
from apps.core.models import Author
from apps.posts.serializers import PostSerializer, LikeSerializer
from rest_framework import status
import json
from socialdistribution.utils import Utils
# Create your views here.

class inbox(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str):
        try:
            if (not Author.objects.get(pk=author_id)):
                return Http404()
        except:
            return Http404()

        host = request.scheme + "://" + request.get_host()

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

        formatted_data = Utils.formatResponse(query_type="GET on index", data=parsed_items)
        result = self.get_paginated_response(formatted_data)
        data = {**data, **result.data} 

        return JsonResponse(data, safe=False)
    def post(self, request: HttpRequest, author_id: str):
        author: Author = None
        try:
            author: Author = Author.objects.get(pk=author_id)
        except:
            return Http404()
        #print("HERE IS THE REQUEST DATA")
        #print(request.data)
        # need to swap this from body to data to fix an error
        #data: dict = json.loads(request.body)
        data: dict = request.data
        if (not data.__contains__("id")):
            HttpResponseBadRequest("Body must contain the id of the item")
        if (not data.__contains__("type")):
            HttpResponseBadRequest("Body must contain the type of the item")
        
        host = request.scheme + "://" + request.get_host()
        if data["type"] == InboxItem.ItemTypeEnum.POST:
            serializer = PostSerializer(data=data)
        elif data["type"] == InboxItem.ItemTypeEnum.FOLLOW:
            # TODO: Follow serializer here
            serializer = None
        elif data["type"] == InboxItem.ItemTypeEnum.LIKE:
            serializer = LikeSerializer(data=data, context={'host': host})
        else:
            HttpResponseBadRequest(data["type"] + "Is not a known type of inbox item")

        if (serializer and not serializer.is_valid()):
            return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        existing = None

        try:
            existing = InboxItem.objects.get(item_id=data["id"], author_id=author_id)
        except InboxItem.DoesNotExist:
            pass

        if (existing != None):
            existing.delete()

        item_content = json.dumps(data, default=lambda x: x.__dict__)
        item = InboxItem.objects.create(author_id=author, item_id=data["id"], item_type=data["type"], item=item_content)
        item.save()

        formatted_data = Utils.formatResponse(query_type="POST on inbox", data=item_content)
        return Response(formatted_data, status=status.HTTP_201_CREATED)

    def delete(self, request: HttpRequest, author_id: str):
        try:
            if (not Author.objects.get(pk=author_id)):
                return Http404()
        except:
            return Http404()

        items = InboxItem.objects.filter(author_id=author_id)

        if (items):
            for item in items:
                item.delete()
            return HttpResponse()
        else:
            return HttpResponseNotFound()


# Examples of calling api
# author uuid(replace): "4f890507-ad2d-48e2-bb40-163e71114c27"
# post uuid(replace): "d57bbd0e-185c-4964-9e2e-d5bb3c02841a"
# Authentication admin(replace): "YWRtaW46YWRtaW4=" (admin:admin)

# GET
# curl 127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/inbox

# POST
# curl http://127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/inbox -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{"type":"post","title":"A Friendly post title about a post about web dev","id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e","source":"http://lastplaceigotthisfrom.com/posts/yyyyy","origin":"http://whereitcamefrom.com/posts/zzzzz","description":"This post discusses stuff -- brief","contentType":"text/plain","content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan","author":{"type":"author","id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e","host":"http://127.0.0.1:5454/","displayName":"Lara Croft","url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e","github": "http://github.com/laracroft","profileImage": "https://i.imgur.com/k7XVwpB.jpeg"},"categories":["web","tutorial"],"comments":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments","published":"2015-03-09T13:07:04+00:00","visibility":"FRIENDS","unlisted":false}'  
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

# DELETE
# curl -X DELETE http://127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/inbox -H "Authorization: Basic YWRtaW46YWRtaW4="