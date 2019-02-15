from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Category
from ..serializers import CategorySerializer


class CategoryView(generics.GenericAPIView):
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)



