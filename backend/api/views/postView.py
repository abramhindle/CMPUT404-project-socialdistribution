from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models.authorModel import Author
from ..models.postModel import Post
from rest_framework import status
from ..serializers import PostSerializer
from ..utils import getPaginatedObject, handlePostImage


@api_view(['POST', 'GET'])
def PostList(request, author_uuid):
  try:  # try to get the specific author
      authorObject = Author.objects.get(uuid=author_uuid)
  except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)

  # Create a new post
  if request.method == 'POST':
    try:  # try to get the image handled data
      request_data = handlePostImage(request.data)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # get the Post serializer
    serializer = PostSerializer(data=request_data)

    # update the Post data if the serializer is valid
    if serializer.is_valid():
      serializer.save(author=authorObject)
      return Response({"message": "Post created", "data": serializer.data}, 
        status=status.HTTP_201_CREATED)

    # return an error if something goes wrong with the update
    return Response({"message": serializer.errors}, 
      status=status.HTTP_400_BAD_REQUEST)

  # List all the posts
  elif request.method == 'GET':
    try:  # try to get the posts
        posts = Post.objects.filter(author=author_uuid).order_by('id')
    except:  # return an error if something goes wrong
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get the paginated posts
    paginated_posts = getPaginatedObject(request, posts)

    # get the Post serializer
    serializer = PostSerializer(paginated_posts, many=True)

    # create the `type` field for the Posts data
    new_data = {'type': "posts"}

    # add the `type` field to the Posts data
    new_data.update({
        'items': serializer.data,
    })

    # return the updated Posts data
    return Response(new_data, status=status.HTTP_200_OK)

  # Handle unaccepted methods
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def PostDetail(request, author_uuid, post_uuid):
  try:  # try to get the specific author
    authorObject = Author.objects.get(uuid=author_uuid)
  except:  # return an error if something goes wrong
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  # List a specific post
  if request.method == 'GET':
    try:  # try to get the specific post
      post = Post.objects.get(author=author_uuid, uuid=post_uuid)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)
    
    # get the Post serializer
    serializer = PostSerializer(post, many=False)

    # return the Post data
    return Response(serializer.data, status=status.HTTP_200_OK)

  # Update a specific post
  elif request.method == 'POST':
    try:  # try to get the specific post & image handled data
      post = Post.objects.get(author=author_uuid, uuid=post_uuid)
      request_data = handlePostImage(request.data)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)
    
    # get the Post serializer
    serializer = PostSerializer(instance=post, data=request_data)

    # update the Post data if the serializer is valid
    if serializer.is_valid():
      serializer.save()
      return Response({"message": "Post updated", "data": serializer.data}, 
        status=status.HTTP_200_OK)

    # return an error if something goes wrong with the update
    return Response({"message": serializer.errors}, 
      status=status.HTTP_400_BAD_REQUEST)
  
  # Create a specific post
  elif request.method == 'PUT':
    try:  # try to get the image handled data
      request_data = handlePostImage(request.data)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # get the Post serializer
    serializer = PostSerializer(data=request_data)

    # update the Post data if the serializer is valid
    if serializer.is_valid():
      serializer.save(uuid=post_uuid, author=authorObject)
      return Response({"message": "Post created", "data": serializer.data}, 
        status=status.HTTP_201_CREATED)

    # return an error if something goes wrong with the update
    return Response({"message": serializer.errors}, 
      status=status.HTTP_400_BAD_REQUEST)

  # Delete a specific post
  elif request.method == 'DELETE':
    try:  # try to get the specific post
      post = Post.objects.get(author=author_uuid, uuid=post_uuid)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)
    
    # delete the post
    post.delete()

    # return a deletion message
    return Response({"message": "Post deleted"}, 
      status=status.HTTP_204_NO_CONTENT)

  # Handle unaccepted methods
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
