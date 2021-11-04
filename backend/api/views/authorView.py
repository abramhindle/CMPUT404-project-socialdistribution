from ..models.authorModel import Author
from ..serializers import AuthorSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utils import getPaginatedObject


@api_view(['GET'])
def AuthorList(request):
    # List all the authors
    if request.method == 'GET':
      try:  # try to get the authors
          authors = Author.objects.all()
      except:  # return an error if something goes wrong
          return Response(status=status.HTTP_400_BAD_REQUEST)
      
      # get the paginated posts
      paginated_authors = getPaginatedObject(request, authors)

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


@api_view(['GET', 'POST'])
def AuthorDetail(request, authorUUID):
  try:  # try to get the specific author
      author = Author.objects.get(uuid=authorUUID)
  except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)

  # List a specific author
  if request.method == 'GET':
    # get the Author serializer
    serializer = AuthorSerializer(author, many=False)

    # return the Author data
    return Response(serializer.data, status=status.HTTP_200_OK)

  # Create a specific author
  elif request.method == 'POST':
    # get the Author serializer
    serializer = AuthorSerializer(instance=author, data=request.data)

    # update the Author data if the serializer is valid
    if serializer.is_valid():
      serializer.save()
      return Response({"status": 0, "message": "Author updated"})

    # return an error if something goes wrong with the update
    return Response({"status": 1, "message": "Something went wrong with the update"}, 
      status=status.HTTP_400_BAD_REQUEST)


def AuthorJSONID(authorID):
    try:
        author = Author.objects.get(authorID=authorID)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AuthorSerializer(author)
    return Response(serializer.data)

