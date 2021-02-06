from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello there! This is the index of Social Distribution Backend!!!!")
