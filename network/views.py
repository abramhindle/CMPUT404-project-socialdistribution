from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from network.models import *
from .serializers import *
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
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(authors, many=True)
        new_data = {'type': "authors"}
        new_data.update({
            'items': serializer.data,
        })
        return Response(new_data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def AuthorDetail(request, author_uuid):
#   try:
#     apikey = request.query_params['apikey']
#   except:
#     return Response(status=status.HTTP_401_UNAUTHORIZED)
  
  if request.method == 'GET':
    try:
      author = Author.objects.get(uuid=author_uuid)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AuthorSerializer(author, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

  elif request.method == 'PUT':
    author = Author.objects.get(uuid=author_uuid)
    serializer = AuthorSerializer(instance=author, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({"status": 0, "message": "Author updated"})

    return Response({"status": 1, "message": "Something went wrong with the update"}, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    author = Author.objects.get(uuid=author_uuid)
    author.delete()

    return Response({"status": 0, "message": "Author deleted"}, status=status.HTTP_204_NO_CONTENT)
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def FollowerList(request, author_uuid):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # List all the followers
    if request.method == 'GET':
        # if invalid_auth:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            followers = Author.objects.get(uuid=author_uuid).followers.all()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(followers, many=True)
        new_data = {'type': "followers"}
        new_data.update({
            'items': serializer.data,
        })
        return Response(new_data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def FollowerDetail(request, author_uuid, follower_uuid):
  
  if request.method == 'GET':
    try:
      follower = Author.objects.get(uuid=author_uuid).followers.get(uuid=follower_uuid)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AuthorSerializer(follower, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

  elif request.method == 'PUT':
    follower = Author.objects.get(uuid=author_uuid).followers.get(uuid=follower_uuid)
    serializer = AuthorSerializer(instance=follower, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({"status": 0, "message": "Follower updated"})

    return Response({"status": 1, "message": "Something went wrong with the update"}, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    follower = Author.objects.get(uuid=author_uuid).followers.get(uuid=follower_uuid)
    follower.delete()

    return Response({"status": 0, "message": "Follower deleted"}, status=status.HTTP_204_NO_CONTENT)
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def PostList(request, author_uuid):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # List all the followers
    if request.method == 'GET':
        
        try:
            posts = Post.objects.filter(author=author_uuid)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(posts, many=True)
        new_data = {'type': "posts"}
        new_data.update({
            'items': serializer.data,
        })
        return Response(new_data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def PostDetail(request, author_uuid, post_uuid):
  
  if request.method == 'GET':
    try:
      post = Post.objects.get(author=author_uuid, uuid=post_uuid)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

  elif request.method == 'PUT':
    post = Post.objects.get(author=author_uuid, uuid=post_uuid)
    serializer = PostSerializer(instance=post, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({"status": 0, "message": "Post updated"})

    return Response({"status": 1, "message": "Something went wrong with the update"}, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    post = Post.objects.get(author=author_uuid, uuid=post_uuid)
    post.delete()

    return Response({"status": 0, "message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def CommentList(request, author_uuid, post_uuid):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    try:
      page = int(request.query_params['page'])
    except:
      page = 1

    page_size = 5

    # List all the followers
    if request.method == 'GET':
        
        try:
            # https://docs.djangoproject.com/en/3.2/topics/db/queries/#limiting-querysets
            comments = Comment.objects.filter(author=author_uuid, post=post_uuid)[:page_size]
            post = Comment.objects.filter(author=author_uuid, post=post_uuid)[0].post.id
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comments, many=True)
        new_data = {'type': 'comments', 'page': page, 'size': page_size, 'post': post, 'id': post + 'comments' }
        new_data.update({
            'comments': serializer.data,
        })
        return Response(new_data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def CommentDetail(request, author_uuid, post_uuid, comment_uuid):
  
  if request.method == 'GET':
    try:
      comment = Comment.objects.get(author=author_uuid, post=post_uuid, uuid=comment_uuid)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

  elif request.method == 'PUT':
    comment = Comment.objects.get(author=author_uuid, post=post_uuid, uuid=comment_uuid)
    serializer = CommentSerializer(instance=comment, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({"status": 0, "message": "Comment updated"})

    return Response({"status": 1, "message": "Something went wrong with the update"}, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    comment = Comment.objects.get(author=author_uuid, post=post_uuid, uuid=comment_uuid)
    comment.delete()

    return Response({"status": 0, "message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def LikeList(request, author_uuid, post_uuid, comment_uuid=None):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    try:
        post = Post.objects.get(author=author_uuid, uuid=post_uuid)
        if comment_uuid != None:
          comment = Comment.objects.get(author=author_uuid, post=post_uuid, uuid=comment_uuid)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # List all the followers
    if request.method == 'GET':
        try:
            # https://docs.djangoproject.com/en/3.2/topics/db/queries/#limiting-querysets
            host = Author.objects.get(uuid=author_uuid).host.removesuffix('/')
            object_path = host + request.get_full_path().split('/likes')[0]
            # make sure object_path ends with a '/'
            object_path += '/' if (not object_path.endswith('/')) else ''
            likes = Like.objects.filter(author=author_uuid, object=object_path)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LikeSerializer(likes, many=True)
        new_data = {'type': 'likes' }
        new_data.update({
            'items': serializer.data,
        })
        return Response(new_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def UserPost(request, format='json'):
  serializer = UserSerializer(data=request.data)
  if serializer.is_valid():
      user = serializer.save()
      if user:
          token = Token.objects.create(user=user)
          json = serializer.data
          json['token'] = token.key
          print(token.key)
          return Response(json, status=status.HTTP_201_CREATED)

  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserCreate(APIView):
    """ 
    Creates the user. 
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)