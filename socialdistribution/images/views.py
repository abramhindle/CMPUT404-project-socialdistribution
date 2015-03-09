from django.contrib.auth import (authenticate,
                                 login as auth_login, logout as auth_logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from PIL import Image


from django.core.urlresolvers import reverse 
from images.models import Image 
from images.forms import DocumentForm

import logging
logger = logging.getLogger(__name__)

def upload(request):
	imgForm= DocumentForm()
	return render(request,"uploadImage.html", {'imgForm' : imgForm})

def create(request):
	logger.error(request.FILES['thumb'])	
	if request.method =='POST':
		profile = DocumentForm(request.POST, request.FILES)
		if profile.is_valid():         
			if 'thumb' in request.FILES:
				profile.picture = request.FILES['thumb']
				profile.save()
	return render_to_response("display.html")
	'''
    if request.method =='POST':
        profile = DocmentForm(data=request.POST,request.FILES)
        if profile.is_valid():
            
	
	if 'thumb' in request.FILES:
		profile.picture = request.FILES['thumb']
		profile.save()
'''