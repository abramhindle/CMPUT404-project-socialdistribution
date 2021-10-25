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
		'Author List':'/authors/',
        'Author Detail':'/author/<str:pk>/',
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
        
        try:
            authors = Author.objects.all()
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(authors, many=True)
        new_data = {'type': "authors"}
        new_data.update({
            'items': serializer.data,
        })
        return Response(new_data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def AuthorDetail(request, pk):
#   try:
#     apikey = request.query_params['apikey']
#   except:
#     return Response(status=status.HTTP_401_UNAUTHORIZED)
  
  if request.method == 'GET':
    try:
      author = Author.objects.get(uuid=pk)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AuthorSerializer(author, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

  elif request.method == 'PUT':
    author = Author.objects.get(uuid=pk)
    serializer = AuthorSerializer(instance=author, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({"status": 0, "message": "Author updated"})

    return Response({"status": 1, "message": "Something went wrong with the update"}, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    author = Author.objects.get(uuid=pk)
    Author.delete()

    return Response({"status": 0, "message": "Author deleted"}, status=status.HTTP_204_NO_CONTENT)
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
