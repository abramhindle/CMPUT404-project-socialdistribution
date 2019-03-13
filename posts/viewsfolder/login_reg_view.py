from django.views.generic import TemplateView
from posts.serializers import UserSerializer
from django.shortcuts import render


class RegistrationPageView(TemplateView):

    def get(self, request):
        return render(request, 'users/register.html')

class LoginPageView(TemplateView):
	def get(self, request):
		return render(request, 'users/login.html')
