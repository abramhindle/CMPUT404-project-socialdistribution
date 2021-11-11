from django.shortcuts import render
from django.views import generic
from django.template import loader
from .models import InboxItem

def index(request):
    inbox = InboxItem.objects.all()
    print("HERE IS THE REQUEST")
    print(request)
    template = loader.get_template('inbox/index.html')
    context={'inboxitems',inbox}
    return render(request,'inbox/index.html',context)    