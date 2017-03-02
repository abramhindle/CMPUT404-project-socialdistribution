from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views import generic

# Create your views here.


def index(request):
    if not request.user.is_authenticated():
        return render_to_response('landing/index.html', locals())
    else:
        return render_to_response('dashboard/index.html', locals())
