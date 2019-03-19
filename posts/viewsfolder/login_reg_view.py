from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework import views
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response


class RegistrationPageView(TemplateView):

    def get(self, request):
        return render(request, 'users/register.html')


class LoginPageView(views.APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/posts/')
        else:
            return render(request, 'users/login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_approved():
                login(request, user)
                return redirect("/posts/")
            else:
                messages.error(request, "User is not approved")
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            messages.error(request, 'username or password not correct')
            return Response(status=status.HTTP_400_BAD_REQUEST)
