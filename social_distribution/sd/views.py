from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
import os
import pdb

def get_page_info(request):
	"""gross temporary code to be replaced with regex in the future"""
	path = request.get_full_path()
	if('page=') in path:
		num = path.split('page=')[1]
	else:
		return 0, 10
	if('&' in num):
		page_num = num.split('&')[0]
	else:
		page_num = num
	temp = path.split('size=')
	if len(temp)>1:
		size=temp[1]
	try:
		size = int(size)
		assert(size>=1)
	except:
		size = 10
	try:
		page_num = int(page_num)
		assert(page_num>=0)
	except:
		page_num=0
	return page_num, size

def index(request):
	return redirect('explore', permanent=True)

def login(request):
	return HttpResponse("Login Page")

def create_account(request):
	return HttpResponse("Create Account Page")

def requests(request):
	return HttpResponse("Friend Requests Page")

def feed(request):
	return HttpResponse("Your Feed")

def explore(request):
	feed = Post.objects.all()
	page_num, size = get_page_info(request)
	print("Page number=%d, size=%d" % (page_num, size))
	page = 'sd/index.html'
	# pdb.set_trace()
	v = list(feed)
	return render(request, page, {'feed':v})

def author(request, author_id):
	try:
		author = Author.objects.get(uuid=author_id)
	except:
		raise Exception(404)
	return HttpResponse(author.username+"'s Page")

def post(request, post_id):
	try:
		post = Post.objects.get(uuid=post_id)
	except:
		raise Exception(404)
	return HttpResponse("Post Page")

def post_comment(request, post_id):
	comments = Comment.objects.filter(post=post_id)
	return HttpResponse("Post Comments Page")

def friends(request):
	return HttpResponse("Friends Page")

# def search(request):
# 	return HttpResponse("User Search Page")


# def account(request):
# 	return HttpResponse("Your Account Page")