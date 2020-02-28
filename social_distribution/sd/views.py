from django.http import HttpResponse
from django.shortcuts import render
import os

def login(request):
	return HttpResponse("Login Page")

def create_account(request):
	return HttpResponse("Create Account Page")

def forgot_pass(request):
	return HttpResponse("Forgotten Password Page")

def home(request):
	page = os.getcwd()+'/sd/sites/sandbox.html'
	return render(request, page)

def search(request):
	return HttpResponse("User Search Page")

def friends(request):
	return HttpResponse("Friends Page")

def requests(request):
	return HttpResponse("Friend Requests Page")

def account(request):
	return HttpResponse("Your Account Page")