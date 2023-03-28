from rest_framework import generics
from rest_framework.response import Response
from .serializers import AuthorSerializer, FollowSerializer, PostsSerializer, ImageSerializer, CommentsSerializer, LikeSerializer, InboxSerializer, NodeSerializer
from .models import AuthorModel, FollowModel, PostsModel, CommentsModel, LikeModel, InboxModel, NodeModel
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from .utils import build_author_url, build_post_url, build_comment_url
from django.http import HttpResponse, JsonResponse
import base64
import re
import os
import requests


class PermittedForRemote(BasePermission):
    """
    Custom permission class that determines permissions based on the endpoint
    the request is accessing.
    
    This is intended to be used in a decorator like this:
        @permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
    
    When used in such a decorator, it's like a janky way of saying, "you can
    only use this endpoint's method if you're either an admin or an an
    authenticated remote node. In the latter case, you can only access a subset
    of the endpoint's methods."
    This allows us to just set our frontend as an admin user so it can access
    all the endpoints it needs to, while restricting other nodes (authenticated
    non-admins) to endpoint methods marked 'remote' in the spec. This is
    probably a terrible way of accomplishing this. Feel free to make better
    (perhaps an API token would be a better solution for the frontend.)
    """

    remote_views = {'GET': ['AuthorsView', 'AuthorView', 'FollowersView',
                            'AuthorFollowersOperationsView', 'PostsView',
                            'PostView', 'CommentsView', 'PostLikeView',
                            'LikeView', 'GetLikeCommentView', 'LikedView',
                            'CommentLikeView', 'LikedView', 'FollowView', 'ImageView'],
                    'POST': ['InboxView']}      # XXX: There's some funky stuff in the spec for POSTing to the inbox and likes endpoint. May cause problems later. See: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#inbox and https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#likes
    def has_permission(self, request, view):
        name = view.__class__.__name__
        return name in self.remote_views[request.method]
    
    
class NodeView(generics.GenericAPIView):
    """
    Hacky stuff. Make a request to a node on behalf of poor soul blocked by cors.
    
    e.g.
    POST "https://sd16-api.herokuapp.com/service/nodes/",
        auth=('admin','123'),
        data={'host':"https://sd7-api.herokuapp.com",
        "resource":"/api/authors/",
        "query":"?page=1&size=25&query="}).json()
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = NodeModel.objects.all()
    serializer_class = NodeSerializer
    
    def post(self, request, *args, **kwargs):
        node = self.queryset.filter(node_url=request.data.get('host', '')).first()
        
        serializer = self.serializer_class(node)
        if not node:
            return Response(status=404)
        
        methods = {'GET': requests.get, 'POST':requests.post, 'PUT':requests.put}
        uri = serializer.data['node_url'] + request.data.get('resource', '/') + request.data.get('query', '')
        print(uri, request.data.get('method', 'GET'), request.data.get('data', ''))
        r = methods[request.data.get('method', 'GET')](uri, data=request.data.get('data', ''), auth=(serializer.data['t16_uname'], serializer.data['t16_pw']))
        return JsonResponse(r.json())


class AuthorView(generics.RetrieveUpdateAPIView):
    """
    Class for handling a single author
    
    URL: ://service/authors/{AUTHOR_ID}/
        GET [local, remote]: retrieve AUTHOR_ID’s profile
        POST [local]: update AUTHOR_ID’s profile
    
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#single-author
        
    Example Format:
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]
    queryset = AuthorModel.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        author_id = kwargs.pop('author_id', None)
        author = self.queryset.filter(id=build_author_url(author_id)).first()
        if not author:
            return Response(status=404)
        serializer = self.serializer_class(author)
        serializer.data['profileImage'] = serializer.data['id'] + '/image'
        return Response(serializer.data)
    
    # FIXME: Why this still put? should be post according to spec.
    def put(self, request, *args, **kwargs):
        author_id = kwargs.pop('author_id', None)
        author = self.queryset.filter(id=build_author_url(author_id)).first()
        if not author:
            return Response(status=404)
        serializer = self.serializer_class(author, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=400)

        
class AuthorsView(generics.ListCreateAPIView):
    """
    Class for handling authors, with pagination and query params
    
    URL: ://service/authors/
        GET [local, remote]: retrieve all profiles on the server (paginated)
            page: how many pages
            size: how big is a page
    Example query: GET ://service/authors?page=10&size=5
        Gets the 5 authors, authors 45 to 49.   
         
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#authors
 
    Example: GET ://service/authors/
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]
    queryset = AuthorModel.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        # return all authors based on the page, size and query params
        page = int(request.query_params.get('page', 1))
        size = int(request.query_params.get('size', 10))
        page = page if page > 0 else 1
        size = size if size > 0 else 10

        query = request.query_params.get('query', '')
        try:
            authors = self.queryset.filter(displayName__icontains=query)[(page-1)*size:page*size]
        except IndexError:
            ## get all authors
            authors = self.queryset.filter(displayName__icontains=query)
        serializer = self.serializer_class(authors, many=True)
        authors_data = serializer.data[::-1]
        for author in authors_data:
            author['profileImage'] = author['id'] + '/image'
        return Response({
            "type": "authors",
            "items": authors_data,
        })
    
    def post(self, request, *args, **kwargs):
        if request.data.get('id'):
            request.data['id'] = build_author_url(request.data['id'])
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class FollowersView(generics.ListAPIView):
    """
    Class for handling followers of a given author
    
    URL: ://service/authors/{AUTHOR_ID}/followers
        GET [local, remote]: get a list of authors who are AUTHOR_ID’s followers
        
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#followers
 
    Example: GET ://service/authors/{AUTHOR_ID}/followers
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]
    queryset = FollowModel.objects.all()
    serializer_class = FollowSerializer

    def get(self, request, *args, **kwargs):
        # find all followers of a given author_id in the url
        author_id = kwargs['author_id']
        author_id = build_author_url(author_id)

        
        follows = self.queryset.filter(follower=author_id)
        ## go through all followers and get the author object
        ## and add it to the list of followers
        followers_list = []
        for follow in follows:
            if follow.status == 'pending':
                continue
            author = AuthorSerializer(AuthorModel.objects.filter(id=follow.following).first()).data
            followers_list.append(author)
        
        return Response({
            "type": "followers",
            "items": followers_list,
        })
        

class FollowView(generics.RetrieveUpdateDestroyAPIView):
    """
    Class for handling follows, can be used to create a new follow, get a follow, update a follow, delete a follow based on a given author_id and foreign_author_id.
    
    URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
        DELETE [local]: remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
        PUT [local]: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
        GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
            
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#followers
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]
    queryset = FollowModel.objects.all()
    serializer_class = FollowSerializer

    def get(self, request, *args, **kwargs):
        # find the follow object with the given author_id and follower_id
        follower_id = kwargs['author_id']
        following_id = kwargs['foreign_author_id']
        
        follower_id = build_author_url(follower_id)
        following_id = build_author_url(following_id)
        follow = self.queryset.filter(follower=follower_id, following=following_id).first()
        other_follow = self.queryset.filter(following=follower_id, follower=following_id).first()
        
        if follow and other_follow:
            status = self.serializer_class(follow).data['status']
            other_status = self.serializer_class(other_follow).data['status']
            if status == 'friends' and other_status == 'friends':
                return Response('true_friends')
            elif status == 'pending' or other_status == 'pending':
                return Response('pending')
            elif status == 'not_friends' or other_status == 'not_friends':
                return Response('not_friends')
        
        if not follow:
            return Response({'detail': 'Follow not found.'}, status=404)
        serializer = self.serializer_class(follow)
        return Response(serializer.data['status'])
        
    def put(self, request, *args, **kwargs):
        # find the follow object with the given author_id and follower_id
        follower_id = kwargs['author_id']
        following_id = kwargs['foreign_author_id']

        follower_id = build_author_url(follower_id)
        following_id = build_author_url(following_id)
        
        follow = self.queryset.filter(follower=follower_id, following=following_id).first()
        if not follow:
            return Response({'detail': 'Follow not found.'}, status=404)
        
        serializer = self.serializer_class(follow, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        # find the follow object with the given author_id and follower_id
        follower_id = kwargs['author_id']
        following_id = kwargs['foreign_author_id']

        follower_id = build_author_url(follower_id)
        following_id = build_author_url(following_id)

        follow = self.queryset.filter(follower=follower_id, following=following_id).first()
        if not follow:
            return Response({'detail': 'Follow not found.'}, status=404)
        follow.delete()
        return Response(status=204)

    @staticmethod
    def create_follow(data, **kwargs):
        follower_id = kwargs['author_id']
        following_id = kwargs['foreign_author_id']
        if 'http' not in follower_id:
            follower_id = build_author_url(follower_id)
        if 'http' not in following_id:
            following_id = build_author_url(following_id)
        
        follow_data = {
            'follower': follower_id,
            'following': following_id,
            'status': 'pending'
        }
        
        serializer = FollowSerializer(data=follow_data)
        if serializer.is_valid():
            serializer.save()


## post view can be used to create a new post, get a post, update a post, delete a post
class PostView(generics.RetrieveUpdateDestroyAPIView, generics.ListCreateAPIView):
    """
    Class for handling posts, can be used to create a new post, get a post, update a post, delete a post based on a given post_id.
    
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
        GET [local, remote] get the public post whose id is POST_ID
        POST [local] update the post whose id is POST_ID (must be authenticated)
        DELETE [local] remove the post whose id is POST_ID
        PUT [local] create a post where its id is POST_ID
        
    Be aware that Posts can be images that need base64 decoding.
        posts can also hyperlink to images that are public
            
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#post
 
    Example Format:
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]
    queryset = PostsModel.objects.all()
    serializer_class = PostsSerializer

    def get(self, request, *args, **kwargs):
        # find the post with the given post_id
        
        post_id = kwargs['post_id']
        author_id = kwargs['author_id']
        post_id = build_post_url(author_id, post_id)

        post = self.queryset.filter(id=post_id).first()
        if not post:
            return Response({'detail': 'Post not found.'}, status=404)
        serializer = self.serializer_class(post)

        comment_count = CommentsModel.objects.filter(post=post_id).count()
        
        data = dict(serializer.data)
        data['count'] = comment_count
        if data.get('contentType', '') == 'image/*':
            data['content'] = data['id'] + '/image'
        return Response(data)
        
    def put(self, request, *args, **kwargs):
        # find the post with the given post_id
        post_id = kwargs['post_id']
        author_id = kwargs['author_id']
        post_id = build_post_url(author_id, post_id)
        author_id = build_author_url(author_id)

        post = self.queryset.filter(id=post_id).first()
        author = AuthorModel.objects.filter(id=author_id).first()
        if not post:
            return Response({'detail': 'Post not found.'}, status=404)
        
        if post.author.id != author_id:
            return Response({'detail': 'You are not the author of this post.'}, status=403)
        
      
        request.data['author'] = AuthorSerializer(author).data
        serializer = self.serializer_class(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        # find the post with the given post_id
        post_id = kwargs['post_id']
        author_id = kwargs['author_id']

        post_id = build_post_url(author_id, post_id)
        post = self.queryset.filter(id=post_id).first()
        if not post:
            return Response({'detail': 'Post not found.'}, status=404)
        post.delete()
        return Response(status=204)
    
    def post(self, request, *args, **kwargs):
        post_id = kwargs.pop('post_id', None)
        author_id = kwargs['author_id']

        post_id = build_post_url(author_id, post_id)
        author_id = build_author_url(author_id)

        author = AuthorModel.objects.filter(id=author_id).first()
        if not author:
            return Response({'detail': 'Author not found.'}, status=404)
        if post_id:
            request.data['id'] = post_id
        request.data['author'] = AuthorSerializer(author).data
      
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PostsView(generics.ListCreateAPIView):
    """
    Class for handling the posts of a given author, can be used to create a new post or get all posts of a given author
    
    Creation URL ://service/authors/{AUTHOR_ID}/posts/
        GET [local, remote] get the recent posts from author AUTHOR_ID (paginated)
        POST [local] create a new post but generate a new id
    Be aware that Posts can be images that need base64 decoding.
        posts can also hyperlink to images that are public
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]
    queryset = PostsModel.objects.all()
    serializer_class = PostsSerializer

    def get(self, request, *args, **kwargs):
        # find all posts of a given author_id in the url
        author_id = kwargs['author_id']
        author_id = build_author_url(author_id)
        author = AuthorModel.objects.filter(id=author_id).first()
        posts = self.queryset.filter(author=author)
        
        page = int(request.query_params.get('page', 0))
        size = int(request.query_params.get('size', 10))
        page = max(page, 0)
        size = max(size, 1)
        
        serializer = self.serializer_class(posts, many=True)
        if size > len(serializer.data):
            size = len(serializer.data)

        ## get the comments for each post
        for post in serializer.data:
            post_id = post['id']

            post_comments = CommentsModel.objects.filter(post=post_id)
            post_comments = CommentsSerializer(post_comments, many=True)
            post['commentsSrc'] = {
                "type": "comments",
                "comments": post_comments.data[:10],
                "page": 1,
                "size": min(len(post_comments.data), 10),
            }
            print(post['contentType'])
            if post['contentType'] == 'image/*':
                post['content'] = post['id'] + '/image'
            post['count'] = min(len(post_comments.data), 10)

        return Response({
            "type": "posts",
            "items": serializer.data[ page * size : (page + 1) * size ][::-1],
        })

    def post(self, request, *args, **kwargs):
        author_id = kwargs.pop('author_id', None)
        author_id = build_author_url(author_id)
        
        author = AuthorModel.objects.filter(id=author_id).first()
        if not author:
            return Response({'detail': 'Author not found.'}, status=404)
        request.data['author'] = AuthorSerializer(author).data

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ImageView(generics.RetrieveAPIView):
    """
    Class for returning the image data of an author or post.
    
    If you go to this url in browser, it should display only the image.
    The HTTP response only contains the image portion of the post. This only
    applies to images hosted on our node. Image links from other domains do not
    count for this endpoint.

    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/image
        GET [local, remote] get the public post converted to binary as an image
            return 404 if not an image
    URL: ://service/authors/{AUTHOR_ID}/image
        GET [local, remote] get the author's profile image converted to binary
    This end point decodes image posts as images. This allows the use of image tags in markdown.
    You can use this to proxy or cache images.
        
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#image-posts
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]

    def get(self, request, *args, **kwargs):
        url_id = request.build_absolute_uri().split('/image')[0] 
        print(url_id)
        author = AuthorModel.objects.filter(id=url_id).first()
        post = PostsModel.objects.filter(id=url_id).first() 
        
        if not author and not post:
            return Response("Image not found", status=404)
        
        if not author:
            if post.contentType.startswith('image') and 'link' not in post.contentType:
                image_data = post.content.partition('base64,')[2]
                binary = base64.b64decode(image_data)
                return HttpResponse(binary, content_type="image/png")
            else:
                return HttpResponse("Not an image", status=400)
        elif not post:
            image_data = author.profileImage.partition('base64,')[2]
            binary = base64.b64decode(image_data)
            return HttpResponse(binary, content_type="image/png")
        

class CommentsView(generics.ListCreateAPIView):
    """
    Class for handling the comments of a given post, can be used to create a new comment or get all comments of a given post
    
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
        GET [local, remote] get the list of comments of the post whose id is POST_ID (paginated)
        POST [local] if you post an object of “type”:”comment”, it will add your comment to the post whose id is POST_ID
            
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#comments

    example comment from ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]
    queryset = CommentsModel.objects.all()
    serializer_class = CommentsSerializer

    def get(self, request, *args, **kwargs):
        # find all comments of a given post_id in the url
        post_id = kwargs['post_id']
        author_id = kwargs['author_id']
        post_id = build_post_url(author_id, post_id)
        post = PostsModel.objects.filter(id=post_id).first()
        page = int(request.query_params.get('page', 1))
        size = int(request.query_params.get('size', 10))
        page = max(page, 1)
        size = max(size, 1)
        
        try:
            comments = self.queryset.filter(post=post).order_by('-created_at')[size*(page-1):size*page]
        except IndexError:
            ## get all comments if the page is out of range
            comments = self.queryset.filter(post=post).order_by('-created_at')
        serializer = self.serializer_class(comments, many=True)
        return Response({
            "type": "comments",
            "page": page,
            "size": size,
            "post": post_id,
            "id": post_id,
            "comments": serializer.data,
        })

    def post(self, request, *args, **kwargs):
        ## add the comment to the post given the post_id in the url
        post_id = kwargs['post_id']
        author_id = kwargs['author_id']
        post_id = build_post_url(author_id, post_id)
        author_id = build_author_url(author_id)
        post = PostsModel.objects.filter(id=post_id).first()

        if not post:
            return Response({'detail': 'Post not found.'}, status=404)
        
        request.data['post'] = PostsSerializer(post).data
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    

class LikeView(generics.ListCreateAPIView):
    """
    Class for handling the likes of a given post, can be used to get all likes of a given post
    
    You can like posts and comments
    Send them to the inbox of the author of the post or comment
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
        GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID
            
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#likes

    Example like object:
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]
    queryset = LikeModel.objects.all()
    serializer_class = LikeSerializer

    def get(self, request, *args, **kwargs):
        # find all likes of a given post_id in the url
        post_id = kwargs['post_id']
        post_id = build_post_url(kwargs['author_id'], post_id)
        post = PostsModel.objects.filter(id=post_id).first()
        if not post:
            return Response({'detail': 'Post not found.'}, status=404)
        likes = self.queryset.filter(post=post)
        serializer = self.serializer_class(likes, many=True)
        return Response({
            "type": "likes",
            "post": post_id,
            "items": serializer.data,
        })
    
    def post(self, request, *args, **kwargs):
        object = request.data.get('object', None)
        if not object:
            return Response({'detail': 'Object not found.'}, status=404)
    
        post = PostsModel.objects.filter(id=object).first()
        comment = CommentsModel.objects.filter(id=object).first()

        if not post and not comment:
            return Response({'detail': 'Post or comment not found.'}, status=404)
        if post:
            request.data['post'] = object
        if comment:
            request.data['comment'] = object
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    @staticmethod
    def create_like(data):
        object = data.get('object', None)
        
        if not object:
            raise Exception({'detail': 'Object not found.'})

        post = PostsModel.objects.filter(id=object).first()
        comment = CommentsModel.objects.filter(id=object).first()
        data['type'] = 'like'

        if not post and not comment:
            raise Exception({'detail': 'Post or comment not found.'})
        if post:
            data['post'] = object
        if comment:
            data['comment'] = object
        
        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            
            serializer.save()
        else:
            raise Exception(serializer.errors)
        

class GetLikeCommentView(generics.ListAPIView):
    """
    Class for handling the likes of a given comment, can be used to get all likes of a given comment
    
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
        GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID comment COMMENT_ID
            
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#likes

    Example like object:
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]
    queryset = LikeModel.objects.all()
    serializer_class = LikeSerializer

    def get(self, request, *args, **kwargs):
        # find all likes of a given comment_id in the url
        comment_id = kwargs['comment_id']
        comment_id = build_comment_url(kwargs['author_id'], kwargs['post_id'], comment_id)
        likes = self.queryset.filter(comment=comment_id)
        serializer = self.serializer_class(likes, many=True)
        return Response({
            "type": "likes",
            "comment": comment_id,
            "items": serializer.data,
        })


class LikedView(generics.ListAPIView):
    """
    Class for handling the likes of a given post, can be used to get all likes of a given post
    
    URL: ://service/authors/{AUTHOR_ID}/liked
        GET [local, remote] list what public things AUTHOR_ID liked.
            It’s a list of of likes originating from this author
                
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#liked

    Example liked object:
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]
    queryset = LikeModel.objects.all()
    serializer_class = LikeSerializer

    def get(self, request, *args, **kwargs):
        # ffind all likes of an author given the author_id in the url
        author_id = kwargs['author_id']
        author_id = build_author_url(author_id)

        author = AuthorModel.objects.filter(id=author_id).first()

        likes = self.queryset.filter(author=author)
        serializer = self.serializer_class(likes, many=True)
        return Response({
            "type": "likes",
            "items": serializer.data,
        })
    

## create InboxView, capabe of handling GET, DELETE, POST requests
class InboxView(generics.ListCreateAPIView, generics.DestroyAPIView):
    """
    Class for handling the inbox of a given author, can be used to get all inbox items of a given author, delete all inbox items of a given author, or create a new inbox item for a given author
    
    The inbox is all the new posts from who you follow
    URL: ://service/authors/{AUTHOR_ID}/inbox
        GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
        POST [local, remote]: send a post to the author
            if the type is “post” then add that post to AUTHOR_ID’s inbox
            if the type is “follow” then add that follow is added to AUTHOR_ID’s inbox to approve later
            if the type is “like” then add that like to AUTHOR_ID’s inbox
            if the type is “comment” then add that comment to AUTHOR_ID’s inbox
        DELETE [local]: clear the inbox
            
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#inbox

    Example, retrieving an inbox
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser|IsAuthenticated&PermittedForRemote]
    queryset = InboxModel.objects.all()
    serializer_class = InboxSerializer

    def get(self, request, *args, **kwargs):
        # find all inbox items of a given author_id in the url
        
        author_id = kwargs['author_id']
        ## only get the object column.
        #FollowModel.objects.all().delete()
        #InboxModel.objects.all().delete()
        inbox = self.queryset.filter(author=build_author_url(author_id)).values_list('object', 'type')
        
        for val in inbox:
            val[0]['type'] = val[1]
        inbox = [val[0] for val in inbox]
        
        return Response({
            "type": "inbox",
            "items":inbox[::-1]
        })
    
    def post(self, request, *args, **kwargs):
        # add the inbox item to the author given the author_id in the url
        author_id = kwargs['author_id']
        
        author_id = build_author_url(author_id)
        author = AuthorModel.objects.filter(id=author_id).first()
        if not author:
            return Response({'detail': 'Author not found.'}, status=404)

        if request.data.get('type', '').lower() == 'like':
            data_like = request.data
            try:
                LikeView.create_like(data_like)
            except Exception as e:
                return Response(str(e), status=400)
        
        elif request.data.get('type', '').lower() == 'follow':
            data_follow = request.data
            
            foreign_author_id = data_follow.get('actor', {}).get('id')

            try:
                FollowView.create_follow(data_follow, **{
                    'author_id': author_id,
                    'foreign_author_id': foreign_author_id
                })
            except Exception as e:
                return Response(str(e), status=400)

        author_data = request.data.get('author', None)

        if author_data and request.data.get('type', '').lower() != 'post':
            ## we dont want to add to our own inbox
            if author_data.get('id', None) == author_id:
                return Response({}, status=201)
        author_serialized = AuthorSerializer(author)
        
        # start hacky stuff
        post_link = request.data.get('object', '')
        if post_link:
            if 'sd7' in post_link:
                r = requests.get(post_link, auth=(os.getenv('T7_UNAME'), os.getenv('T7_PW')))
                object_data = r.json()
        else:
            object_data = request.data
        # object_data = request.data
        # end hacky stuff
        
        data = {
            'object': object_data,
            'type': request.data.get('type', ''),
            'author': author_serialized.data
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        # delete all inbox items of a given author_id in the url
        author_id = kwargs['author_id']
        author_id = build_author_url(author_id)
        author = AuthorModel.objects.filter(id=author_id).first()
        inbox = self.queryset.filter(author=author)
        inbox.delete()
        return Response(status=204)
