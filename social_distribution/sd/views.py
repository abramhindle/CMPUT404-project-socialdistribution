from django.http import HttpResponse
from django.shortcuts import render
import os

def index(request):
	"""
	# check cookie for logged in  and user details
	# if logged in, go to /me/posts
	# else go to a global list of public posts 
	"""
	return HttpResponse("Redirect")

def login(request):
	return HttpResponse("Login Page")

def create_account(request):
	return HttpResponse("Create Account Page")

def forgot_pass(request):
	return HttpResponse("Forgotten Password Page")

def home(request):
	page = os.getcwd()+'/sd/templates/sd/index.html'
	return render(request, page)

def search(request):
	return HttpResponse("User Search Page")

def friends(request):
	return HttpResponse("Friends Page")

def requests(request):
	return HttpResponse("Friend Requests Page")

def account(request):
	return HttpResponse("Your Account Page")