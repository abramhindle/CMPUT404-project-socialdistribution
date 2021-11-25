from django.http.request import HttpRequest
from django.shortcuts import render
from django.views import generic
from .models import Author
from apps.posts.models import Post
from socialdistribution.utils import Utils

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'core/index.html'

def authors(request: HttpRequest):
    if request.user.is_anonymous:
        return render(request,'core/index.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    authors = Author.objects.all()
    # Todo: Add authors from other hosts
    host = request.scheme + "://" + request.get_host()
    context = {
        'is_staff': request.user.is_staff,
        'author' : currentAuthor, 
        'authors': authors, 
        'host':host}
    return render(request, 'authors/index.html', context)

def author(request: HttpRequest, author_id: str):
    currentAuthor=Author.objects.filter(userId=request.user).first()

    if request.user.is_anonymous or (currentAuthor.id != author_id and not request.user.is_staff):
        return render(request,'core/index.html')

    host = request.scheme + "://" + request.get_host()
    context = {
        'author_id': currentAuthor.id,
        'is_staff': request.user.is_staff,
        'target_author_id' : author_id,
        'host':host
    }
    return render(request,'authors/author.html',context)