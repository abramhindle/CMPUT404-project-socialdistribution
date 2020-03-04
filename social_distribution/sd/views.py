from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
import os

BASE = "127.0.0.1/8000/sd/"

def index(request):
	"""
	# check cookie for logged in  and user details
	# if logged in, go to /me/posts
	# else go to a global list of public posts 
	"""
	return redirect('home', permanent=True)

def login(request):
	return HttpResponse("Login Page")

def create_account(request):
	return HttpResponse("Create Account Page")

def forgot_pass(request):
	return HttpResponse("Forgotten Password Page")

def home(request):
	feed = Post.objects.all()
	page = 'sd/index.html'
	return render(request, page, {'feed':feed})

def search(request):
	return HttpResponse("User Search Page")

def friends(request):
	return HttpResponse("Friends Page")

def requests(request):
	return HttpResponse("Friend Requests Page")

def account(request):
	return HttpResponse("Your Account Page")

def feed(request):
	return HttpResponse("Your Feed")

def explore(request):
	return HttpResponse("Public Posts")

def author(request, author_id):
	author = Author.objects.get(uuid=author_id)
	return HttpResponse(author.username+"'s Page")