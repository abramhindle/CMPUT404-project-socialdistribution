from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.list import ListView
from follow.models import AlreadyExistsError, Follow, Request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q


USER_MODEL = get_user_model()


def get_follow_list():
    return getattr(settings, "FOLLOW_LIST", "users")


def create_follow_request(request, to_username):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    to_user = USER_MODEL.objects.get(username=to_username)
    from_user = request.user
    try:
        Follow.objects.follow_request(from_user, to_user)
    except AlreadyExistsError as e1:
        pass
    except ValidationError as e2:
        pass
    finally:
        return redirect(to_user.get_absolute_url())


def accept_follow_request(request, from_username):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    from_user = USER_MODEL.objects.get(username=from_username)
    to_user = request.user
    try:
        request_accept = Request.objects.get(from_user=from_user, to_user=to_user)
        request_accept.accept()
        request_accept.save()
    except AlreadyExistsError:
        pass
    finally:
        return redirect(from_user.get_absolute_url())


def reject_follow_request(request, from_username):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    from_user = USER_MODEL.objects.get(username=from_username)
    to_user = request.user
    try:
        request_accept = Request.objects.get(from_user=from_user, to_user=to_user)
        request_accept.reject()
    except ValidationError as e2:
        pass
    finally:
        return redirect(from_user.get_absolute_url())


def unfollow_request(request, from_username):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    from_user = USER_MODEL.objects.get(username=from_username)
    try:
        Follow.objects.unfollow(follower=request.user, followee=from_user)
    except AlreadyExistsError as e1:
        pass
    except ValidationError as e2:
        pass
    finally:
        return redirect(from_user.get_absolute_url())


class UsersView(LoginRequiredMixin, ListView):
    model = USER_MODEL
    template_name = 'follow/user_list.html'

    def get_queryset(self):
        return USER_MODEL.objects.filter(~Q(pk=self.request.user.id) & Q(is_staff=False))


class FriendRequestsView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'follow/request_list.html'

    def get_queryset(self):
        return Request.objects.filter(to_user=self.request.user)


class MyFriendsView(LoginRequiredMixin, ListView):
    model = USER_MODEL
    template_name = 'follow/friend_list.html'

    def get_queryset(self):
        return Follow.objects.true_friend(self.request.user)
