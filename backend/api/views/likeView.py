from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models.likeModel import Like
from ..models.authorModel import Author
from ..models.commentModel import Comment
from ..models.postModel import Post
from rest_framework import status
from ..utils import getPageNumber, getPageSize, getPaginatedObject, loggedInUserExists, getLoggedInAuthorObject, postToAuthorInbox
from ..serializers import LikeSerializer


@api_view(['POST', 'GET'])
def LikeListPost(request, author_uuid, post_uuid):
  try:  # try to get the specific author and post
      postObject = Post.objects.get(author=author_uuid, uuid=post_uuid)
  except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)

  # Create a new like
  if request.method == 'POST':
    # if the logged in user does not exist
    if not loggedInUserExists(request):  
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:  # if the logged in user exists
      loggedInAuthorObject = getLoggedInAuthorObject(request)
      # if the logged in user does not have an Author object
      if loggedInAuthorObject is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # get the Like serializer
    serializer = LikeSerializer(data=request.data)

    # update the Like data if the serializer is valid
    if serializer.is_valid():
      serializer.save(author=loggedInAuthorObject, 
        summary=(loggedInAuthorObject.displayName + " likes your post"), 
        object=postObject.id
      )
      postToAuthorInbox(request, serializer.data, author_uuid)
      return Response({"message": "Like created", "data": serializer.data}, 
        status=status.HTTP_201_CREATED)

    # return an error if something goes wrong with the update
    return Response({"message": serializer.errors}, 
      status=status.HTTP_400_BAD_REQUEST)
  
  # List all the likes
  if request.method == 'GET':
    try:  # try to get the likes
        likes = Like.objects.filter(author=author_uuid, object=postObject.id)
    except:  # return an error if something goes wrong
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get the page number and size
    page_number = getPageNumber(request)
    page_size = getPageSize(request)

    # get the paginated likes
    paginated_likes = getPaginatedObject(likes, page_number, page_size)

    # get the Like serializer
    serializer = LikeSerializer(paginated_likes, many=True)

    # create the `type` field for the Likes data
    new_data = {'type': "likes"}

    # add the `type` field to the Likes data
    new_data.update({
        'items': serializer.data,
    })

    # return the updated Likes data
    return Response(new_data, status=status.HTTP_200_OK)

  # Handle unaccepted methods
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST', 'GET'])
def LikeListComment(request, author_uuid, post_uuid, comment_uuid):
  try:  # try to get the specific author, post and comment
      Post.objects.get(author=author_uuid, uuid=post_uuid)
      commentObject = Comment.objects.get(author=author_uuid, 
        post=post_uuid, uuid=comment_uuid)
  except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)

  # Create a new like
  if request.method == 'POST':
    # if the logged in user does not exist
    if not loggedInUserExists(request):  
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:  # if the logged in user exists
      loggedInAuthorObject = getLoggedInAuthorObject(request)
      # if the logged in user does not have an Author object
      if loggedInAuthorObject is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # get the Like serializer
    serializer = LikeSerializer(data=request.data)

    # update the Like data if the serializer is valid
    if serializer.is_valid():
      serializer.save(author=loggedInAuthorObject, 
        summary=(loggedInAuthorObject.displayName + " likes your comment"), 
        object=commentObject.id
      )
      postToAuthorInbox(request, serializer.data, author_uuid)
      return Response({"message": "Like created", "data": serializer.data}, 
        status=status.HTTP_201_CREATED)

    # return an error if something goes wrong with the update
    return Response({"message": serializer.errors}, 
      status=status.HTTP_400_BAD_REQUEST)
  
  # List all the likes
  if request.method == 'GET':
    try:  # try to get the likes
        likes = Like.objects.filter(author=author_uuid, 
          object=commentObject.id)
    except:  # return an error if something goes wrong
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get the page number and size
    page_number = getPageNumber(request)
    page_size = getPageSize(request)

    # get the paginated likes
    paginated_likes = getPaginatedObject(likes, page_number, page_size)

    # get the Like serializer
    serializer = LikeSerializer(paginated_likes, many=True)

    # create the `type` field for the Likes data
    new_data = {'type': "likes"}

    # add the `type` field to the Likes data
    new_data.update({
        'items': serializer.data,
    })

    # return the updated Likes data
    return Response(new_data, status=status.HTTP_200_OK)

  # Handle unaccepted methods
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
