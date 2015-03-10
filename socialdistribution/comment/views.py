from django.shortcuts import render
from django.template import RequestContext


def create_comment(request):
    context = RequestContext(request)