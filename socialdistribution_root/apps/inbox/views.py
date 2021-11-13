from django.db.models.fields.related import ForeignKey
from django.db.models.query import RawQuerySet
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views import generic
from django.template import loader
from .models import InboxItem
from django.http.request import HttpRequest
from apps.core.models import Author

def index(request: HttpRequest):
    inbox = InboxItem.objects.all()
    currentAuthor=Author.objects.filter(userId=request.user).first()
    template = loader.get_template('inbox/index.html')
    context={'inboxitems':inbox,'author_id':currentAuthor.id}
    return render(request,'inbox/index.html',context)    