from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.template.loader import get_template
from django.contrib.auth import views as AuthViews
from socialdistribution.utils import Utils

def error_404(request, exception):
    context = {}
    return render(request, '404.html', context)

class LogoutView(AuthViews.LogoutView):
    def get(self, request, *args, **kwargs):
        self.extra_context = { 'allowSignUp': Utils.allowsSignUp() }
        return super().get(request, *args, **kwargs)

class LoginView(AuthViews.LoginView):
    def get(self, request, *args, **kwargs):
        self.extra_context = { 'allowSignUp': Utils.allowsSignUp() }
        return super().get(request, *args, **kwargs)

class PasswordResetConfirmView(AuthViews.PasswordResetConfirmView):
    def get(self, request, *args, **kwargs):
        self.extra_context = { 'allowSignUp': Utils.allowsSignUp() }
        return super().get(request, *args, **kwargs)

class PasswordResetCompleteView(AuthViews.PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        self.extra_context = { 'allowSignUp': Utils.allowsSignUp() }
        return super().get(request, *args, **kwargs)

class PasswordResetDoneView(AuthViews.PasswordResetDoneView):
    def get(self, request, *args, **kwargs):
        self.extra_context = { 'allowSignUp': Utils.allowsSignUp() }
        return super().get(request, *args, **kwargs)

class PasswordResetView(AuthViews.PasswordResetView):
    def get(self, request, *args, **kwargs):
        self.extra_context = { 'allowSignUp': Utils.allowsSignUp() }
        return super().get(request, *args, **kwargs)