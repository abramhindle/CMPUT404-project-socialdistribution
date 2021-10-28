from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import generic
from .models import User as Author
from rest_framework import viewsets
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'core/index.html'


