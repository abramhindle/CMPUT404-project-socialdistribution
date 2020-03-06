from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
import os
import pdb

def get_page_info(request):
	path = request.get_full_path()
	num = path.split('page=')[1]
	page_num=1
	size=10
	if('&' in num):
		page_num = num.split('&')[0]
	temp = path.split('size=')
	if len(temp)>1:
		size=temp[1]
	return page_num, size

def index(request):
	return redirect('explore', permanent=True)

def login(request):
	return HttpResponse("Login Page")

def create_account(request):
	return HttpResponse("Create Account Page")

def requests(request, page_num=1, size=10):
	return HttpResponse("Friend Requests Page")

def feed(request, page_num=1, size=10):
	return HttpResponse("Your Feed")

def explore(request):
	feed = Post.objects.all()
	page_num, size = get_page_info(request)
	print("PAGE NUMBER:", page_num)
	print('SIZE:', size)
	page = 'sd/index.html'
	return render(request, page, {'feed':feed})

def author(request, author_id, page_num=1, size=10):
	author = Author.objects.get(uuid=author_id)
	return HttpResponse(author.username+"'s Page")

def post(request, post_id, page_num=1, size=10):
	post = Post.objects.get(uuid=post_id)
	return HttpResponse(post)

def post_comment(request, post_id, page_num=1, size=10):
	post = Comment.objects.get(post=post_id)
	return HttpResponse(post)

def friends(request, page_num=1, size=10):
	return HttpResponse("Friends Page")

# def search(request):
# 	return HttpResponse("User Search Page")


# def account(request):
# 	return HttpResponse("Your Account Page")