from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from follow.models import AlreadyExistsError, Follow, Request
from django.contrib.auth import get_user_model
# Create your views here.
USER_MODEL = get_user_model()


def get_follow_list():
    return getattr(settings, "FOLLOW_LIST", "users")


def all_users_list(request):
    users = USER_MODEL.objects.all()
    user_list = [_.username for _ in users if _.username != request.user.username]
    print(user_list)

    followings = Follow.objects.followings(user=request.user)
    followers = Follow.objects.followers(user=request.user)
    request_list = Request.objects.request(user=request.user)
    print(request_list)
    return render(
        request, template_name="./all_users.html", context={get_follow_list(): list(set(user_list) - set(followings)),
                                                            "followings": followings,
                                                            "followers": followers,
                                                            "request_list": request_list
                                                            }
    )


def create_follow_request(request, to_username):
    payload = {"to_username": to_username}
    if request.method == 'POST':
        to_user = USER_MODEL.objects.get(username=to_username)
        from_user = request.user
        try:
            Follow.objects.follow_request(from_user, to_user)
        except AlreadyExistsError as e1:
            payload["error"] = str(e1)
        except ValidationError as e2:
            payload["error"] = str(e2)
        else:
            return redirect("/")  # TODO need to be update

    return render(request, template_name='./create_follow_request.html', context=payload)


def accept_follow_request(request, from_username):
    payload = {"from_username": from_username}
    if request.method == 'POST':
        from_user = USER_MODEL.objects.get(username=from_username)
        to_user = request.user
        try:
            request_accept = Request.objects.get(from_user=from_user, to_user=to_user)
            request_accept.accept()
            request_accept.save()
        except AlreadyExistsError as e1:
            payload["error"] = str(e1)
        except ValidationError as e2:
            payload["error"] = str(e2)
        else:
            return redirect("/")  # TODO need to be update
    return render(request, template_name='./accept_follow_request.html', context=payload)


def reject_follow_request(request, from_username):
    payload = {"from_username": from_username}
    if request.method == 'POST':
        from_user = USER_MODEL.objects.get(username=from_username)
        to_user = request.user
        try:
            request_accept = Request.objects.get(from_user=from_user, to_user=to_user)
            request_accept.reject()
        except ValidationError as e2:
            payload["error"] = str(e2)
        else:
            return redirect("/")  # TODO need to be update
    return render(request, template_name='./reject_follow_request.html', context=payload)


def unfollow_request(request, from_username):
    payload = {"from_username": from_username}
    if request.method == 'POST':
        from_user = USER_MODEL.objects.get(username=from_username)
        to_user = request.user
        try:
            Follow.objects.unfollow(from_user, to_user)
        except AlreadyExistsError as e1:
            payload["error"] = str(e1)
        except ValidationError as e2:
            payload["error"] = str(e2)
        else:
            return redirect("/")  # TODO need to be update
    return render(request, template_name='./unfollow_request.html', context=payload)


def remove_follow_request(request, to_username):
    payload = {"to_username": to_username}
    if request.method == 'POST':
        to_user = USER_MODEL.objects.get(username=to_username)
        from_user = request.user
        try:
            Follow.objects.unfollow(from_user, to_user)
        except AlreadyExistsError as e1:
            payload["error"] = str(e1)
        except ValidationError as e2:
            payload["error"] = str(e2)
        else:
            return redirect("/")  # TODO need to be update
    return render(request, template_name='./remove_follow_request.html', context=payload)
