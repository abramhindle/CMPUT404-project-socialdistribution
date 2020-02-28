from django.http import HttpResponse
from django.shortcuts import render, redirect
import os

ok_header = bytearray("""HTTP/1.1 200 OK\r\n""",'utf-8')
bad_method_header = bytearray("""HTTP/1.1 405 Method Not Allowed\r\n\r\n""", 'utf-8')
not_found_header = bytes("""HTTP/1.1 404 Not Found\r\n""", 'utf-8')
redirect_header = bytearray("""HTTP/1.1 301 Moved Permanently\r\n""", "utf-8")

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