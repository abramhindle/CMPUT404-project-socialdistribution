from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Author
from posts.forms import PostForm
from .forms import ProfileForm

from django.views.decorators.csrf import csrf_exempt
import base64

def index(request):
    author = Author.objects.get(displayName='Xiaole')   #hardcode here

    context = {
        'author': author,
    }

    return render(request, 'profiles/index_base.html', context)

@csrf_exempt
def new_post(request):
    form = PostForm()
    author = Author.objects.get(displayName='Xiaole')

    context = {
        'form': form,
        'author': author,
    }

    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_content = form.save(commit=False)
            cont_type = form.cleaned_data['content_type']
            if(cont_type == "image/png;base64" or cont_type == "image/jpeg;base64" ):
                img = form.cleaned_data['image_file']
                new_content.content = base64.b64encode(img.file.read())

            new_content.save()
            url = reverse('index')
            return HttpResponseRedirect(url)

    return render(request, 'posts/posts_form.html', context)

def current_visible_posts(request):
    return HttpResponse("Only these posts are visible to you: ")


def author_posts(request, author_id):
    return HttpResponse("Here are the posts of %s: ", author_id)

def view_profile(request):
    author = Author.objects.get(displayName= 'Xiaole')

    context = {
        'author': author,
    }
    return render(request, 'profiles/profiles_view.html', context)


def edit_profile(request):
    author = Author.objects.get(displayName='Xiaole')   #hardcode here
    form = ProfileForm(request.POST or None, request.FILES or None, instance=author)

    context = {
        'form': form,
        'author': author,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            url = reverse('editprofile')
            return HttpResponseRedirect(url)

    return render(request, 'profiles/profiles_edit.html', context)
