from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import AuthorModel, PostsModel, CommentsModel, LikeModel
from ..serializers import PostsSerializer, AuthorSerializer, CommentsSerializer, LikeSerializer
import json
import uuid

@api_view(['GET', 'POST'])
def AuthorView(request, uid):
    """
    API endpoint that allows users to be viewed or edited.
    ---
    # YAML
    
    type:
        name:
            required:
        type:
    url:
        required:
        type:
    created_at:
        required:
        type:
        format:
        
    serializer:
    omit_serializer: false
    many:
    
    parameters_strategy: merge
    omit_parameters:
    parameters:
    
    responseMessage:
        - code:
        message:
    
    consumes:
    
    produces:
    """
    if request.method == 'GET':
        author_object = AuthorModel.objects.get(id=uid)
        serialized_object = AuthorSerializer(author_object)
        output = serialized_object.data
        return JsonResponse(output, status = 200)
    elif request.method == 'POST':
        author_object = AuthorModel.objects.get(id=uid)
        serialized_object = AuthorSerializer(author_object)
        parameters = json.loads(request.body)
        serialized_object.update(author_object, parameters)
        output = serialized_object.data
        return JsonResponse(output, status = 200)
    
    
@api_view(['GET'])
def AuthorsView(request):
    """
    API endpoint that allows users to be viewed.
    ---
    # YAML
    
    type:
        name:
            required:
        type:
    url:
        required:
        type:
    created_at:
        required:
        type:
        format:
        
    serializer:
    omit_serializer: false
    many:
    
    parameters_strategy: merge
    omit_parameters:
    parameters:
    
    responseMessage:
        - code:
        message:
    
    consumes:
    
    produces:
    """
    page = int(request.GET.get('page', '1'))
    size = int(request.GET.get('size', '5'))
    authors_list = AuthorModel.objects.order_by('-displayName')[page*size-5:page*size-1]
    # print(authors_list)
    serialized_authors_list = list([AuthorSerializer(author).data for author in authors_list])
    output = {
    "type": "authors",      
    "items": serialized_authors_list,
    }
    return JsonResponse(output, status = 200)