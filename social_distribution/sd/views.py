from django.http import HttpResponse

def login(request):
	return HttpResponse("Login Page")

def create_account(request):
	return HttpResponse("Create Account Page")

def forget_pass(request):
	return HttpResponse("Forgotten Password Page")

def home(request):
	return HttpResponse("Home Page")

def search(request):
	return HttpResponse("User Search Page")

def friends(request):
	return HttpResponse("Friends Page")

def requests(request):
	return HttpResponse("Friend Requests Page")

def account(request):
	return HttpResponse("Your Account Page")