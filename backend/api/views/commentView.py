from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models.commentModel import Comment
from ..models.authorModel import Author
from ..models.postModel import Post
from rest_framework import status
from ..utils import getPageNumber, getPageSize, getPaginatedObject, loggedInUserExists, loggedInUserIsAuthor, loggedInUserHasId, getLoggedInAuthorObject, postToAuthorInbox
from ..serializers import CommentSerializer


@api_view(['POST', 'GET'])
def CommentList(request, author_uuid, post_uuid):
  try:  # try to get the specific authors and post
      Author.objects.get(uuid=author_uuid)
      postObject = Post.objects.get(author=author_uuid, uuid=post_uuid)
  except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)

  # Create a new comment
  if request.method == 'POST':
    # if the logged in user does not exist
    if not loggedInUserExists(request):  
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:  # if the logged in user exists
      loggedInAuthorObject = getLoggedInAuthorObject(request)
      # if the logged in user does not have an Author object
      if loggedInAuthorObject is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # get the Comment serializer
    serializer = CommentSerializer(data=request.data)

    # update the Comment data if the serializer is valid
    if serializer.is_valid():
      serializer.save(author=loggedInAuthorObject, post=postObject)
      postToAuthorInbox(request, serializer.data, author_uuid)
      return Response({"message": "Comment created", "data": serializer.data}, 
        status=status.HTTP_201_CREATED)

    # return an error if something goes wrong with the update
    return Response({"message": serializer.errors}, 
      status=status.HTTP_400_BAD_REQUEST)

  # List all the comments
  elif request.method == 'GET':
    try:  # try to get the comments
        comments = Comment.objects.filter(post=post_uuid).order_by('id')
    except:  # return an error if something goes wrong
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get the page number and size
    page_number = getPageNumber(request)
    page_size = getPageSize(request)

    # get the paginated comments
    paginated_comments = getPaginatedObject(comments, page_number, page_size)

    # get the Comment serializer
    serializer = CommentSerializer(paginated_comments, many=True)

    # create the `type`, `page` and `size` fields for the Comments data
    new_data = {'type': "comments", "page": page_number, "size": page_size}

    # add the `type` field to the Comments data
    new_data.update({
        'items': serializer.data,
    })

    # return the updated Comments data
    return Response(new_data, status=status.HTTP_200_OK)

  # Handle unaccepted methods
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def CommentDetail(request, author_uuid, post_uuid, comment_uuid):
  # List a specific comment
  if request.method == 'GET':
    try:  # try to get the specific comment
      comment = Comment.objects.get(uuid=comment_uuid)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)
    
    # get the Comment serializer
    serializer = CommentSerializer(comment, many=False)

    # return the Comment data
    return Response(serializer.data, status=status.HTTP_200_OK)

  # Update a specific comment
  elif request.method == 'POST':
    try:  # try to get the specific comment
      comment = Comment.objects.get(uuid=comment_uuid)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)
    
    # if the logged in user is not the author or comment creator
    if not (loggedInUserIsAuthor(request, author_uuid) or loggedInUserHasId(request, comment.author.id)):  
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:  # if the logged in user is the author or comment creator
      loggedInAuthorObject = getLoggedInAuthorObject(request)
      # if the logged in user does not have an Author object
      if loggedInAuthorObject is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # get the Comment serializer
    serializer = CommentSerializer(instance=comment, data=request.data)

    # update the Comment data if the serializer is valid
    if serializer.is_valid():
      serializer.save(author=loggedInAuthorObject)
      return Response({"message": "Comment updated", "data": serializer.data}, 
        status=status.HTTP_200_OK)

    # return an error if something goes wrong with the update
    return Response({"message": serializer.errors}, 
      status=status.HTTP_400_BAD_REQUEST)

  # Delete a specific comment
  elif request.method == 'DELETE':
    try:  # try to get the specific comment
      comment = Comment.objects.get(uuid=comment_uuid)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)
    
    # if the logged in user is not the author or comment creator
    if not (loggedInUserIsAuthor(request, author_uuid) or loggedInUserHasId(request, comment.author.id)):  
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # delete the comment
    comment.delete()

    # return a deletion message
    return Response({"message": "Comment deleted"}, 
      status=status.HTTP_204_NO_CONTENT)
  
  # Handle unaccepted methods
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
