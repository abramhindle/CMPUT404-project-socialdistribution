from ..models.authorModel import Author
from ..serializers import AuthorSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utils import getPageNumber, getPageSize, getPaginatedObject, loggedInUserIsAuthor


@api_view(['GET'])
def AuthorList(request):
  # List all the authors
  if request.method == 'GET':
    try:  # try to get the authors
        authors = Author.objects.all().order_by('id')
    except:  # return an error if something goes wrong
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # get the page number and size
    page_number = getPageNumber(request)
    page_size = getPageSize(request)

    # get the paginated authors
    paginated_authors = getPaginatedObject(authors, page_number, page_size)

    # get the Author serializer
    serializer = AuthorSerializer(paginated_authors, many=True)

    # create the `type` field for the Authors data
    new_data = {'type': "authors"}

    # add the `type` field to the Authors data
    new_data.update({
        'items': serializer.data,
    })

    # return the updated Authors data
    return Response(new_data, status=status.HTTP_200_OK)

  # Handle unaccepted methods
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def AuthorDetail(request, author_uuid):
  try:  # try to get the specific author
      author = Author.objects.get(uuid=author_uuid)
  except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)

  # List a specific author
  if request.method == 'GET':
    # get the Author serializer
    serializer = AuthorSerializer(author, many=False)

    # return the Author data
    return Response(serializer.data, status=status.HTTP_200_OK)

  # Update a specific author
  elif request.method == 'POST':
    # if the logged in user is not the author
    if not loggedInUserIsAuthor(request, author_uuid):  
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # get the Author serializer
    serializer = AuthorSerializer(instance=author, data=request.data)

    # update the Author data if the serializer is valid
    if serializer.is_valid():
      serializer.save()
      return Response({"message": "Author updated", "data": serializer.data}, status=status.HTTP_200_OK)

    # return an error if something goes wrong with the update
    return Response({"message": serializer.errors, "data": serializer.data}, 
      status=status.HTTP_400_BAD_REQUEST)

  # Handle unaccepted methods
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
