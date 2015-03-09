from django.shortcuts import render


def all_visible_posts(request):
    raise NotImplementedError


def post(request, post_id):
    raise NotImplementedError


def posts(request):
    """Return the posts that are visible to the current authenticated user."""
    raise NotImplementedError


def author_posts(request):
    raise NotImplementedError


def profile(request, author):
    raise NotImplementedError


def friends(request, user_id):
    raise NotImplementedError


def is_friend(request, user_id1, user_id2):
    raise NotImplementedError


def friend_request(request):
    raise NotImplementedError
