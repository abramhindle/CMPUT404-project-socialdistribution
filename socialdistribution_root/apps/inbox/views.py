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
    globalInbox = InboxItem.objects.all()
    currentAuthor=Author.objects.filter(userId=request.user).first()
    template = loader.get_template('inbox/index.html')
    currentAuthorInbox = []
    for inboxItem in globalInbox:
        print(inboxItem.author_id)
        authorOfInboxItem = inboxItem.author_id
        allFollowers = authorOfInboxItem.followers.all()
        #print(allFollowers)
        #print(currentAuthor)
        if currentAuthor in allFollowers:
            print("OK!")
            currentAuthorInbox.append(inboxItem)

    context={'inboxitems':currentAuthorInbox}
    return render(request,'inbox/index.html',context)    