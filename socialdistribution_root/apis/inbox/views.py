from django.http.request import HttpRequest
from django.views import View
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from apps.inbox.models import InboxItem
from apis.inbox.dto_models import Inbox
from apps.core.models import Author
import json

# Create your views here.

class inbox(View):
    def get(self, request: HttpRequest, author_id: str):
        try:
            if (not Author.objects.get(pk=author_id)):
                return Http404()
        except:
            return Http404()

        host = request.scheme + "://" + request.get_host()
        
        try:
            items = InboxItem.objects.order_by('created_at').filter(author_id=author_id)
            return HttpResponse(Inbox.from_items(host, author_id, items).to_json())
        except InboxItem.DoesNotExist:
            return HttpResponse(Inbox.from_items(host, author_id, []).to_json())

    def post(self, request: HttpRequest, author_id: str):
        author: Author = None
        try:
            author: Author = Author.objects.get(pk=author_id)
        except:
            return Http404()

        data: dict = json.loads(request.body.decode('utf-8'))
        
        if (not data.__contains__("id")):
            HttpResponseBadRequest("Body must contain the id of the item")
        if (not data.__contains__("type")):
            HttpResponseBadRequest("Body must contain the type of the item")
        
        # TODO: additional data validation ?

        if (data["type"] == "post" or data["type"] == "follow" or data["type"] == "like"):
            HttpResponseBadRequest(data["type"] + "Is not a known type of inbox item")

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

        return HttpResponse()

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


# Below are example api calls
# GET
# curl 127.0.0.1:8000/author/838a3993-d399-4ca6-ab00-276c0d02db54/inbox/

# POST
# curl http://127.0.0.1:8000/author/838a3993-d399-4ca6-ab00-276c0d02db54/inbox/ -H "X-CSRFToken: nhSny2B3RUyi8I14uoszEw2NQdoTKnsWM8Yp0u7e9p1erKr01KMSnFl8Xz1Ch2qA" -H "Cookie: csrftoken=nhSny2B3RUyi8I14uoszEw2NQdoTKnsWM8Yp0u7e9p1erKr01KMSnFl8Xz1Ch2qA" -d '{"type":"post","title":"A Friendly post title about a post about web dev","id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e","source":"http://lastplaceigotthisfrom.com/posts/yyyyy","origin":"http://whereitcamefrom.com/posts/zzzzz","description":"This post discusses stuff -- brief","contentType":"text/plain","content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan","author":{"type":"author","id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e","host":"http://127.0.0.1:5454/","displayName":"Lara Croft","url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e","github": "http://github.com/laracroft","profileImage": "https://i.imgur.com/k7XVwpB.jpeg"},"categories":["web","tutorial"],"comments":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments","published":"2015-03-09T13:07:04+00:00","visibility":"FRIENDS","unlisted":false}'  
# curl http://127.0.0.1:8000/author/838a3993-d399-4ca6-ab00-276c0d02db54/inbox/ -H "X-CSRFToken: nhSny2B3RUyi8I14uoszEw2NQdoTKnsWM8Yp0u7e9p1erKr01KMSnFl8Xz1Ch2qA" -H "Cookie: csrftoken=nhSny2B3RUyi8I14uoszEw2NQdoTKnsWM8Yp0u7e9p1erKr01KMSnFl8Xz1Ch2qA" -d '{"type":"post","title":"A post posted with put api on /post/", "id":"22233344559874651687", "description":"This post discusses stuff -- brief","contentType":"text/plain", "author":{ "type":"author","id":"838a3993-d399-4ca6-ab00-276c0d02db54"},"visibility":"PUBLIC",  "unlisted":false}'

# DELETE
# curl -X DELETE http://127.0.0.1:8000/author/838a3993-d399-4ca6-ab00-276c0d02db54/inbox/ -H "X-CSRFToken: nhSny2B3RUyi8I14uoszEw2NQdoTKnsWM8Yp0u7e9p1erKr01KMSnFl8Xz1Ch2qA" -H "Cookie: csrftoken=nhSny2B3RUyi8I14uoszEw2NQdoTKnsWM8Yp0u7e9p1erKr01KMSnFl8Xz1Ch2qA"