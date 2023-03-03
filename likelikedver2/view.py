from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Like

@login_required
def send_like(request, author_id):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        like = Like(post=post, user=request.user)
        like.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request method'})

def get_post_likes(request, author_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    likes = Like.objects.filter(post=post)
    data = [{'author_id': like.user.id, 'display_name': like.user.username, 'profile_image': like.user.profile_image.url} for like in likes]
    return JsonResponse({'likes': data})

def get_comment_likes(request, author_id, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
    likes = Like.objects.filter(comment=comment)
    data = [{'author_id': like.user.id, 'display_name': like.user.username, 'profile_image': like.user.profile_image.url} for like in likes]
    return JsonResponse({'likes': data})

@login_required
def get_liked_items(request, author_id):
    likes = Like.objects.filter(user=request.user)
    data = [{'author_id': like.post.author.id, 'display_name': like.post.author.username, 'profile_image': like.post.author.profile_image.url, 'object': like.post.url} for like in likes]
    return JsonResponse({'items': data})
