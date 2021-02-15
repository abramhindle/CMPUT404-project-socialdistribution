from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status


def Post(request):
    return HttpResponse("<h1> posssssssstT</h1>")
