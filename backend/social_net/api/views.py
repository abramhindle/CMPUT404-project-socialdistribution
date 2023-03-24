from rest_framework import generics
from rest_framework.response import Response
from .serializers import AuthorSerializer, FollowSerializer, PostsSerializer, CommentsSerializer, LikeSerializer, InboxSerializer
from .models import AuthorModel, FollowModel, PostsModel, CommentsModel, LikeModel, InboxModel
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .utils import build_author_url, build_post_url, build_comment_url

class AuthorView(generics.RetrieveUpdateAPIView):
    """
    Class for handling a single author
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = AuthorModel.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        author_id = kwargs.pop('author_id', None)
        author = self.queryset.filter(id=build_author_url(author_id)).first()
        if not author:
            return Response(status=404)
        serializer = self.serializer_class(author)
        return Response(serializer.data)
    
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
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
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
        return Response({
            "type": "authors",
            "items": serializer.data[::-1],
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
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
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
            author = AuthorModel.objects.filter(id=follow.follower).first()
            followers_list.append(author)
        
        serializer = self.serializer_class(followers_list, many=True)
        return Response({
            "type": "followers",
            "items": serializer.data[::-1],
        })
        
class FollowView(generics.RetrieveUpdateDestroyAPIView):
    """
    Class for handling follows, can be used to create a new follow, get a follow, update a follow, delete a follow based on a given author_id and foreign_author_id.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FollowModel.objects.all()
    serializer_class = FollowSerializer

    def get(self, request, *args, **kwargs):
        # find the follow object with the given author_id and follower_id
        follower_id = kwargs['author_id']
        following_id = kwargs['foreign_author_id']
        
        follower_id = build_author_url(follower_id)
        following_id = build_author_url(following_id)
        follow = self.queryset.filter(follower=follower_id, following=following_id).first()
        
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
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
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
        return Response(serializer.data)
        
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
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
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
    

class CommentsView(generics.ListCreateAPIView):
    """
        Class for handling the comments of a given post, can be used to create a new comment or get all comments of a given post
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
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
        author = AuthorModel.objects.filter(id=author_id).first()
        if not post:
            return Response({'detail': 'Post not found.'}, status=404)
        
        request.data['post'] = PostsSerializer(post).data
        request.data['author'] = AuthorSerializer(author).data
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class LikeView(generics.ListCreateAPIView):
    """
        Class for handling the likes of a given post, can be used to get all likes of a given post
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
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
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
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
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
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
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = InboxModel.objects.all()
    serializer_class = InboxSerializer

    def get(self, request, *args, **kwargs):
        # find all inbox items of a given author_id in the url
        
        author_id = kwargs['author_id']
        ## only get the object column.
        
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
        

        author_serialized = AuthorSerializer(author)
        
        if request.data.get('type', '').lower() == 'like':
            data_like = request.data
            try:
                LikeView.create_like(data_like)
            except Exception as e:
                return Response(str(e), status=400)

            #author_data = request.data.pop('author', None)
            #if author_data.get('id', None) == author_id:
            #    return Response({}, status=201)
            
        
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
            
            #author_data = request.data.pop('author', None)
            #if author_data.get('id', None) == author_id:
            #    return Response({}, status=201)

        else:
            #author_data = request.data.pop('author', None)
            #if author_data.get('id', None) == author_id and request.data.get('type', '').lower() != 'post':
            #    return Response({}, status=201)
            pass

        data = {
            'object': request.data,
            'type': request.data.get('type', 'like'),
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
