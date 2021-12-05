from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.template.loader import get_template

def error_404(request, exception):
    context = {}
    return render(request, '404.html', context)