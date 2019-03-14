from django.views.generic import TemplateView
from posts.serializers import UserSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
from rest_framework import views
from django.contrib import messages


class RegistrationPageView(TemplateView):

    def get(self, request):
        return render(request, 'users/register.html')


class LoginPageView(views.APIView):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/posts/")
        else:
            messages.error(request, 'username or password not correct')
