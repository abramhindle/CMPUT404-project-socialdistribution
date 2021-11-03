from ..models.authorModel import Author
from ..serializers import AuthorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def AuthorList(request):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]
    # List all the authors
    if request.method == 'GET':
        try:
            authors = Author.objects.all()
        except:
            return Response(status=400)
        serializer = AuthorSerializer(authors, many=True)
        new_data = {'type': "authors"}
        new_data.update({
            'items': serializer.data,
        })
        return Response(new_data, status=200)


@api_view(['GET', 'PUT', 'DELETE'])
def AuthorDetail(request, authorID):  
  # print(authorID,'AUTHORIDDD')
  if request.method == 'GET':
    try:
      author = Author.objects.get(authorID=authorID)
    except:
        return Response(status=404)
    serializer = AuthorSerializer(author, many=False)
    return Response(serializer.data, status=200)

  elif request.method == 'PUT':
    author = Author.objects.get(authorID=authorID)
    serializer = AuthorSerializer(instance=author, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({"status": 0, "message": "Author updated"})

    return Response({"status": 1, "message": "Something went wrong with the update"}, status=400)

  elif request.method == 'DELETE':
    author = Author.objects.get(authorID=authorID)
    author.delete()

    return Response({"status": 0, "message": "Author deleted"}, status=204)
  else:
    return Response(status=405)


def AuthorJSONID(authorID):
    try:
        author = Author.objects.get(authorID=authorID)
    except:
        return Response(status=404)
    serializer = AuthorSerializer(author)
    return Response(serializer.data)

