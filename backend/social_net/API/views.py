from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import AuthorModel
from .serializers import AuthorSerializer
import json

@api_view(['GET', 'POST'])
def AuthorView(request, uid):
    """
    API endpoint that allows users to be viewed or edited.
    """
    if request.method == 'GET':
        author_object = AuthorModel.objects.get(id=uid)
        serialized_object = AuthorSerializer(author_object)
        return JsonResponse(serialized_object.data, status = 200)

    elif request.method == 'POST':
        author_object = AuthorModel.objects.get(id=uid)
        serialized_object = AuthorSerializer(author_object)
        parameters = json.loads(request.body)
        serialized_object.update(author_object, parameters)
        return JsonResponse(serialized_object.data, status = 200)