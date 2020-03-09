from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
import os
import pdb

def paginated_result(objects, request, keyword, **result):
	page_num = int(request.GET.get('page',0))
	size =     int(request.GET.get('size',10))
	first_result = size*page_num
	count = objects.count()
	if count <= first_result:
		first_result = 0
		page_num = 0
		# JUST SETS TO PAGE 0, we could : Redirect to page 0? 400 Bad Request?
	last_result = first_result + size

	result["count"]    = count
	result["size"]     = size
	result["previous"] = page_num - 1 if page_num >= 1 else None
	result["next"]     = page_num + 1 if objects.count() >= last_result else None
	result[keyword]    = objects[first_result:last_result]
	return result

def index(request):
	return redirect('explore', permanent=True)

def login(request):
	return HttpResponse("Login Page")

def create_account(request):
	return HttpResponse("Create Account Page")

def requests(request):
	return HttpResponse("Friend Requests Page")

def feed(request):
	return HttpResponse("Your Feed")

def explore(request):
	all_posts = Post.objects.all()
	result = paginated_result(all_posts, request, "feed", query="feed")
	return render(request, 'sd/index.html', result)

def author(request, author_id):
	try:
		author = Author.objects.get(uuid=author_id)
	except:
		raise Exception(404)
	return HttpResponse(author.username+"'s Page")

def post(request, post_id):
	try:
		post = Post.objects.get(uuid=post_id)
	except:
		raise Exception(404)
	result = {
		"query" : "post",
		"title" : post.title,
		# "source" : post.source,
		# "description" : post.description,
		# "contentType" : post.contentType,
		"content" : post.body,
		"author": {
			"host": post.author.host,
			"id":  post.author.uuid,
			"url": post.author.uuid, ############ we need a URL
			"displayName":post.author.username, ######## display name???
			"github": post.author.github
		},
		# "categories" : post.categories,
		##### are we implementing comments inside post?
		"published" : post.date,
		"id" : post.uuid,
		"visibleTo" : post.viewable_to
	}
	return HttpResponse("Post Page")
	return render(request, 'sd/index.html', result) ########## posts page

def post_comment(request, post_id):
	comments = Comment.objects.filter(post=post_id)
	result = paginated_result(comments, request, "comments", query="comments")
	return HttpResponse("Post Comments Page")
	return render(request, 'sd/index.html', result) ########## post commments page

def friends(request):
	return HttpResponse("Friends Page")

# def search(request):
# 	return HttpResponse("User Search Page")


# def account(request):
# 	return HttpResponse("Your Account Page")