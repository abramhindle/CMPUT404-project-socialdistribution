from django.shortcuts import render
from django.http import HttpResponse
from .models import Person


# Create your views here.

# To test djongo migration
def home(request):
  
    p = Person(first_name="Akanksha", last_name="Parmar")
    p.save()
    return HttpResponse("Welcome!")
