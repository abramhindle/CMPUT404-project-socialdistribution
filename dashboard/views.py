from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views import generic

# Create your views here.


def index(request):
    return render_to_response('dashboard/index.html', locals())
