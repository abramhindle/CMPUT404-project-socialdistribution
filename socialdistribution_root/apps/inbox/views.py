from django.http.request import HttpRequest
from django.shortcuts import render
from django.views import generic
from django.template import loader
from .models import InboxItem
from django.http.request import HttpRequest

def index(request: HttpRequest):
    inbox = InboxItem.objects.all()
    template = loader.get_template('inbox/index.html')
    context={'inboxitems':inbox}
    return render(request,'inbox/index.html',context)    