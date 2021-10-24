from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from network.models import Author
from .serializers import AuthorSerializer
from rest_framework.decorators import api_view


@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/authors/',
    }
	return Response(api_urls)

@api_view(['GET'])
def AuthorList(request):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # List all the authors
    if request.method == 'GET':
        # if invalid_auth:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # fields = ('__all__')
        try:
            authors = Author.objects.all()
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # serializer = AuthorSerializer(authors, many=True, fields=fields)
        serializer = AuthorSerializer(authors, many=True)
        new_data = {'type': "authors"}
        new_data.update({
            'items': serializer.data,
        })
        return Response(new_data, status=status.HTTP_200_OK)
