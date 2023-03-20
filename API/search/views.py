from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import AuthorModel
from .serializers import AuthorSerializer

@api_view(['GET'])
def SearchView(request):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #checks friendship
    if request.method == 'GET':
        query = request.GET.get('query')
        authors_list = AuthorModel.objects.filter(displayName__icontains=query)
        serialized_authors_list = list([AuthorSerializer(author).data for author in authors_list])
        output = {
        "type": "authors",      
        "items": serialized_authors_list,
        }
        return JsonResponse(output, status = 200)
