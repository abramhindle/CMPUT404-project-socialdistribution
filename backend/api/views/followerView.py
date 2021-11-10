from ..models.authorModel import Author
from ..serializers import AuthorSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utils import getPageNumber, getPageSize, getPaginatedObject, loggedInUserIsAuthor


@api_view(['GET'])
def FollowerList(request, author_uuid):
  # List all the followers
  if request.method == 'GET':
    try:  # try to get the followers
        followers = Author.objects.get(uuid=author_uuid).followers.all()
    except:  # return an error if something goes wrong
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # get the page number and size
    page_number = getPageNumber(request)
    page_size = getPageSize(request)

    # get the paginated followers
    paginated_followers = getPaginatedObject(followers, page_number, page_size)

    # get the Author serializer
    serializer = AuthorSerializer(paginated_followers, many=True)

    # create the `type` field for the Followers data
    new_data = {'type': "followers"}

    # add the `type` field to the Followers data
    new_data.update({
        'items': serializer.data,
    })

    # return the updated Authors data
    return Response(new_data, status=status.HTTP_200_OK)
  
  # Handle unaccepted methods
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'DELETE'])
def FollowerDetail(request, author_uuid, follower_uuid):

  # List a specific follower
  if request.method == 'GET':
    try:  # try to get the specific follower
      follower = Author.objects.get(uuid=author_uuid).followers.get(uuid=follower_uuid)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)

    # get the Author serializer
    serializer = AuthorSerializer(follower, many=False)

    # return the Follower data
    return Response(serializer.data, status=status.HTTP_200_OK)

  # Create a specific follower
  elif request.method == 'PUT':
    # if the logged in user is not the author
    if not loggedInUserIsAuthor(request, author_uuid):  
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    try:  # try to get the author and potential follower
      author = Author.objects.get(uuid=author_uuid)
      follower = Author.objects.get(uuid=follower_uuid)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)

    try:  # try to add the potential follower
      author.followers.append(follower)
      return Response({"message": "Follower created", "data": follower}, 
        status=status.HTTP_201_CREATED)
    except:  # return an error if something goes wrong with the update
      return Response({"message": "something went wrong", 
        "author": author, "follower": follower}, 
        status=status.HTTP_400_BAD_REQUEST)
  
  # Delete a specific follower
  elif request.method == 'DELETE':
    # if the logged in user is not the author
    if not loggedInUserIsAuthor(request, author_uuid):  
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    try:  # try to get the specific follower
      follower = Author.objects.get(uuid=author_uuid).followers.get(uuid=follower_uuid)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)
    
    # delete the follower
    follower.delete()

    # return a deletion message
    return Response({"message": "Follower deleted"}, 
      status=status.HTTP_204_NO_CONTENT)
  
  # Handle unaccepted methods
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
