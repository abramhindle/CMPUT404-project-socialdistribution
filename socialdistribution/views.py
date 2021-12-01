from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.template.loader import get_template

def error_404(request, exception):
    context = {}
    try:
        body = render(request,'404.html')
    except Exception as err:
        print(err)
    return render(request, '404.html', context)