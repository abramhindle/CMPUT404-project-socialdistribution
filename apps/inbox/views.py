from django.db.models.fields.related import ForeignKey
from django.db.models.query import RawQuerySet
from django.http.request import HttpRequest
from django.views import generic
from django.template import loader
from .models import InboxItem
from django.http.request import HttpRequest
from apps.core.models import Author
from socialdistribution.utils import Utils

def index(request: HttpRequest):
    if request.user.is_anonymous or not (request.user.is_authenticated):
        return Utils.defaultRender(request,'posts/index.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    currentAuthorInbox = InboxItem.objects.filter(author_id=currentAuthor)
    host = request.scheme + "://" + request.get_host()
    template = loader.get_template('inbox/index.html')
    context={'inboxitems':currentAuthorInbox, 'author':currentAuthor,'host':host}
    return Utils.defaultRender(request,'inbox/index.html',context)