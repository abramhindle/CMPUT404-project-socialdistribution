from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework import views
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response
from posts.models import WWUser, User
from dispersal.settings import SITE_URL

class RegistrationPageView(TemplateView):

    def get(self, request):
        return render(request, 'users/register.html')


class LoginPageView(views.APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/frontend/posts/feed/')
        else:
            return render(request, 'users/login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Allows superusers to bypass approval process. Doesn't make sense to block them out
            if user.is_approved() or user.is_superuser:
                WWUser.objects.get_or_create(local=True, url=SITE_URL + 'author/{}'.format(user.id), user_id=user.id)
                if not user.is_approved():
                    user.approved = True
                    user.save()

                login(request, user)
                return redirect("/posts/")
            else:
                messages.error(request, "User is not approved")
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            messages.error(request, 'username or password not correct')
            return Response(status=status.HTTP_400_BAD_REQUEST)
