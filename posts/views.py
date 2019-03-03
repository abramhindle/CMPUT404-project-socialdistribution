from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import Http404
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
# Create your views here.


class UserView(views.APIView):

    def get_user(self, user):
        try:
            return User.objects.get(pk=user.pk)
        except User.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'create': True})
        if serializer.is_valid() and request.user.is_anonymous:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(login_required)
    def get(self, request):
        user = self.get_user(request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @method_decorator(login_required)
    def put(self, request):
        user = self.get_user(request.user)
        serializer = UserSerializer(user, data=request.data, partial=True, context={'create':False})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserView(views.APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    @method_decorator(login_required)
    def get(self, request):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        unapproved = User.objects.get(approved=False)

        return Response(data={'unapproved': unapproved}, template_name='approve_user.html')
