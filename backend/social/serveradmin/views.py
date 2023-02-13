from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
 
# Create your views here.
 
 
def image_view(request):
 
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
 
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ImageForm()
    return render(request, 'imageupload.html', {'form': form})
 
 
def success(request):
    return HttpResponse('successfully uploaded')