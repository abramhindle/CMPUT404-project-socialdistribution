from django.shortcuts import render
from django.http import HttpRequest
from post.models import Post



def createPost(request):
    if request.method == "POST":
        text = request.POST.get("text_body", "")
        author = request.POST.get("author", "") #some how get the author
        visibility = request.POST.get("visibility", "")
        mime_type = "text/plain" #not sure whether to determine type or have user input type

        date_now = currentDate() #get current date

        new_post = Post.objects.create(text=text, publication_date=date_now, last_modified=date_now) #TODO: could move in as a default field to fill out


def modifyPost(request):


def deletePost(request):

def index(request):

def posts(request):

def post(request, post_id):