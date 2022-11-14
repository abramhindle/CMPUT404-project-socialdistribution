from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from urllib.parse import urljoin
from rest_framework.views import APIView
from .models import Author, Follow, FollowRequest, Inbox, Post, Node, Like
from .serializers import (AcceptOrDeclineFollowRequestSerializer, 
                          AuthorSerializer, 
                          AuthorRegistrationSerializer, 
                          FollowRequestSerializer, 
                          FollowerSerializer, 
                          SendFollowRequestSerializer, 
                          CreatePostSerializer, 
                          PostSerializer, 
                          UpdatePostSerializer,  
                          SendPrivatePostSerializer,
                          InboxSerializer,
                          RemoveFollowerSerializer,
                          AddNodeSerializer,
                          NodesListSerializer,
                          SendLikeSerializer,
                          PostLikeSerializer,)
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import status, permissions
from django.utils.timezone import utc
import datetime
from .utils import BasicPagination, PaginationHandlerMixin, IsRemoteGetOnly, IsRemotePostOnly, is_remote_request, join_urls
from .api_client import http_request
import logging

logger = logging.getLogger(__name__)
external_request_timeout = 5

class AuthorsView(APIView, PaginationHandlerMixin):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    
    def get_serializer(self, request, queryset):
        return AuthorSerializer(queryset, many=True, context={'request': request})

    def get(self, request):
        authors = Author.objects.exclude(is_remote_user=True).exclude(is_admin=True).order_by("created_at")
        page = self.paginate_queryset(authors)
        if page is not None:
            serializer = self.get_paginated_response(
                self.get_serializer(request, page).data
            )
        else:
            serializer = self.get_serializer(request, authors)

        response_data = serializer.data
        if not is_remote_request(request):
            # TODO: implement synchronicity between local and remote pagination
            external_authors = []
            for node in Node.objects.all():
                # assumes that /authors route applies to all nodes
                url = join_urls(node.api_url, "authors")
                try:
                    response = http_request(method="GET", url=url, timeout=external_request_timeout,
                                            auth=(node.auth_username, node.auth_password))
                    if response == None:
                        continue
                except Exception as e:
                    logger.error("api_client.http_request came across an unexpected error: {}".format(e))
                    continue
                # TODO: convert response to AuthorSerializer format
                external_authors.extend(response)
            
            # serializer.data does not seem to be mutable, so we have to do this (for now...)
            if "results" in serializer.data:
                response_data["results"].extend(external_authors)
            else:
                response_data.extend(external_authors)

        return Response(data=response_data, status=status.HTTP_200_OK)


class AuthorDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsRemoteGetOnly]

    def get_author(self,pk):
        author = get_object_or_404(Author,pk=pk)
        return author

    
    def get(self, request, pk, *args, **kwargs):
        author = self.get_author(pk)
        serializer = AuthorSerializer(author, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request, pk, *args, **kwargs):
        author = self.get_author(pk)
        serializer = AuthorSerializer(instance=author, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorRegistrationView(APIView):
    def post(self, request):
        serializer = AuthorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'message': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login Success'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully Logged out'}, status=status.HTTP_200_OK)


class PostView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsRemoteGetOnly]

    def get_author(self,pk):
        author = get_object_or_404(Author,pk=pk)
        return author
    def get_post(self,post_id,author_id):
        post = get_object_or_404(Post,id=post_id,author=author_id)
        return post
    
    def get(self,request,pk,post_id, *args, **kwargs):
        author =self.get_author(pk)
        post = self.get_post(post_id,author.id)
        if post.visibility == "PUBLIC":
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'requested post is not public'}, status=status.HTTP_400_BAD_REQUEST)
            

    def post(self, request, pk,post_id, *args, **kwargs):
        author = self.get_author(pk)
        post = self.get_post(post_id,author.id)

        if post.visibility == "PUBLIC":   
            if author.id == request.user.id:
                serializer = UpdatePostSerializer(instance=post,data=request.data,partial=True,context={'request': request})
                for field in request.data:
                    if field not in serializer.fields:
                        return Response({'message': 'You cannot edit this field'}, status=status.HTTP_400_BAD_REQUEST)
                if serializer.is_valid():
                    serializer.save(edited_at=datetime.datetime.utcnow().replace(tzinfo=utc))
                    data_dict = {"id":post.id}
                    data_dict.update(serializer.data)
                    return Response(data_dict, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'You cannot edit another authors post'}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'message': 'You can only edit public posts'}, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request,pk,post_id,*args,**kwargs):
        author =self.get_author(pk=pk)
        post = self.get_post(post_id,author.id)
        if post.visibility == "PUBLIC":
            if author.id == request.user.id:
                post.delete()
                return Response({"message":"Object deleted!"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You cannot delete another authors post'}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({'message': 'You can only delete public posts'}, status=status.HTTP_400_BAD_REQUEST)


class AllPosts(APIView, PaginationHandlerMixin):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsRemoteGetOnly]
    pagination_class = BasicPagination

    def get_author(self,pk):
        author = get_object_or_404(Author,pk=pk)
        return author
    
    def get_serializer(self, request, queryset):
        return PostSerializer(queryset, many=True, context={'request': request})

    def get(self, request,pk, *args, **kwargs):
        author = self.get_author(pk)
        posts = author.post_set.all().order_by("-created_at")
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_paginated_response(
                self.get_serializer(request, page).data
            )
        else:
            serializer = self.get_serializer(request, posts)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request, pk, *args, **kwargs):
        author = self.get_author(pk)
        serializer = CreatePostSerializer(data=request.data)
        if author.id == request.user.id:
            if serializer.is_valid():
                new_post = Post.objects.create(
                    author=author,
                    title=serializer.data["title"],
                    description=serializer.data["description"],
                    unlisted=serializer.data["unlisted"],
                    content_type=serializer.data["content_type"],
                    content=serializer.data["content"],
                    visibility=serializer.data["visibility"]
                )
                if new_post.visibility == "FRIENDS":
                    for follow in author.followed_by_authors.iterator():
                        with transaction.atomic():
                            Inbox.objects.create(target_author=follow.follower,post=new_post)
                elif new_post.visibility == "PUBLIC":
                    for author in Author.objects.exclude(username=author.username):
                        with transaction.atomic():
                            Inbox.objects.create(target_author=author,post=new_post)  
                elif new_post.visibility == "PRIVATE":
                    private_post_serializer = SendPrivatePostSerializer(data=request.data)
                    if private_post_serializer.is_valid():
                        
                        try:
                            receiver =  Author.objects.get(pk=private_post_serializer.data['receiver']['id'])    
                        except Author.DoesNotExist:
                            return Response({'message': f'receiver author with id {private_post_serializer.data["receiver"]["id"]} does not exist'}, status=status.HTTP_404_NOT_FOUND)
                        with transaction.atomic():
                            Inbox.objects.create(target_author=receiver, post=new_post)
                                
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                data_dict = {"id":new_post.id}
                data_dict.update(serializer.data)
                return Response(data_dict, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'message': 'You cannot create a post for another user'}, status=status.HTTP_400_BAD_REQUEST)


class AllPublicPostsView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get_serializer(self, request, queryset):
        return PostSerializer(queryset, many=True, context={'request': request})

    def get(self, request):
        """Returns recent public posts"""
        posts = Post.objects.filter(visibility="PUBLIC").order_by("-created_at")
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_paginated_response(
                self.get_serializer(request, page).data
            )
        else:
            serializer = self.get_serializer(request, posts)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorLikedView(APIView):
    authentication_classes = [BasicAuthentication]
    
    def get(self,requst,pk):
        author = get_object_or_404(Author,pk=pk)
        likes = Like.objects.filter(post__visibility="PUBLIC").filter(author=author)
        serializer = PostLikeSerializer(likes, many=True, context={'request': requst})
        # I am doing this so that I can display the post like this "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
        for data in serializer.data: 
            data['post'] = urljoin(data['author']['url'],  f"posts/{data['post']}/")
            
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class PostLikesView(APIView):
    authentication_classes = [BasicAuthentication]
    
    def get(self,requst,pk,post_id):
        author = get_object_or_404(Author,pk=pk)
        post = get_object_or_404(Post,id=post_id,author=author.id)
        likes = Like.objects.filter(post=post.id)
        serializer = PostLikeSerializer(likes, many=True, context={'request': requst})
        # I am doing this so that I can display the post like this "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
        for data in serializer.data: 
            data['post'] = urljoin(data['author']['url'],  f"posts/{data['post']}/")
            
        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowRequestsView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, author_id):
        # TODO: for project part 2; will also need to look at the inbox of this author to fetch follow requests
        # received from remote authors
        author = get_object_or_404(Author, pk=author_id)
        serializer = FollowRequestSerializer(author.follow_requests_received.all(), many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowRequestDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsRemoteGetOnly]
    
    def delete(self, request, author_id, foreign_author_id):
        """Decline a follow request"""
        serializer = AcceptOrDeclineFollowRequestSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: project part 2; foreign author id could be a remote one
            follow_request = get_object_or_404(FollowRequest, sender=foreign_author_id, receiver=author_id)
            follow_request.delete()
            return Response({'message': 'Follow request declined'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowRequestProcessor(object):
    def __init__(self, request, author_id):
        self.request = request
        self.author_id = author_id
        self.response = self.send_request(request, author_id)
    
    def send_request(self, request, author_id):
        serializer = SendFollowRequestSerializer(data=request.data)
        if serializer.is_valid():
            if (serializer.data["sender"]["url"] == serializer.data["receiver"]["url"]):
                return Response(
                    {'message': 'author cannot send follow request to themself'}, status=status.HTTP_400_BAD_REQUEST
                )
            
            # TODO: for project part 2; use the 'url's to determine if a given author is a remote one or a local one
            # if the <host> section of a url is not our host, it's a remote author
            # assume that both the sender and the receiver are local authors for now
            try:
                # TODO: for project part 2; if the receiver is a remote author, we need to send a POST request
                # to the inbox of the remote author; of course we also won't create a local follow request object
                receiver = Author.objects.get(pk=author_id)
            except Author.DoesNotExist:
                return Response({'message': f'author_id {author_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
            try:
                # TODO: for project part 2; if the sender is a remote author, we might need to add another field
                # to the inbox entity 'remote_follow_request_sender_url' to store a local representation of that follow
                # request or find some other solution that works
                sender = Author.objects.get(pk=serializer.data['sender']['id'])
            except Author.DoesNotExist:
                return Response({'message': f'sender author with id {serializer.data["sender"]["id"]} does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)
            
            follow = Follow.objects.filter(follower=sender, followee=receiver)
            if follow.count() > 0:
                return Response({'message': 'sender already follows the receiver'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # https://docs.djangoproject.com/en/4.1/topics/db/transactions/#controlling-transactions-explicitly
                with transaction.atomic():
                    follow_request = FollowRequest.objects.create(sender=sender, receiver=receiver)
                    # update the inbox of the receiver
                    Inbox.objects.create(target_author=receiver, follow_request_received=follow_request)

                # TODO: return the new inbox item when we have an Inbox serializer
                return Response({'message': 'OK'}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'message': 'this follow request already exists'}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_response(self):
        return self.response


class LikePostProcessor(object):
    def __init__(self, request, author_id):
        self.request = request
        self.author_id = author_id
        self.response = self.send_like(request, author_id)
    
    def send_like(self, request, author_id):
        serializer = SendLikeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                post = Post.objects.get(pk=serializer.data['post']['id'])
            except Post.DoesNotExist:
                return Response({'message': f'post with id {serializer.data["post"]["id"]} does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)
            try:   
                author = Author.objects.get(pk=serializer.data['author']['id'])
            except Author.DoesNotExist:
                return Response({'message': f'author with id {serializer.data["author"]["id"]} does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)
            try:
                receiver = Author.objects.get(pk=author_id)
            except Author.DoesNotExist:
                return Response({'message': f'author with id {author_id} does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)
            
            like = Like.objects.filter(author=author,post=post)
            
            if like.count() > 0:
                return Response({'message': 'Cannot like a post more than once'}, status=status.HTTP_400_BAD_REQUEST)
            
            # https://docs.djangoproject.com/en/4.1/topics/db/transactions/#controlling-transactions-explicitly
            with transaction.atomic():
                like = Like.objects.create(author=author,post=post)
                # update the inbox of the receiver
                Inbox.objects.create(target_author=receiver,like=like)
                # TODO: return the new inbox item when we have an Inbox serializer
                
            return Response({'message': 'OK'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_response(self):
        return self.response


class FollowersView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        serializer = FollowerSerializer(author.followed_by_authors.all(), many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowersDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsRemoteGetOnly]
    
    def get(self, request, author_id, foreign_author_id):
        try:
            follow = Follow.objects.get(follower=foreign_author_id, followee=author_id)
            # TODO: return the serialized follow
            return Response({'message': 'follower indeed'}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({'message': f'{foreign_author_id} is not a follower of {author_id}'}, 
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, foreign_author_id):
        if author_id == foreign_author_id:
            return Response({'message': 'author cannot add themself as a follower'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AcceptOrDeclineFollowRequestSerializer(data=request.data)
        if serializer.is_valid():
            # it is safe to assume that the followee will be someone from our server
            # because they are accepting the follow request
            followee = get_object_or_404(Author, pk=author_id)
            
            # TODO: for project part 2; check the 'url' of the follow_request_sender
            # if it's not someone from our server we probably need to save the follower in a different field
            # such as 'remote_follower_url' or find some other solution that works
            
            # assume that foreign_author_id is someone from our server for now
            follower = get_object_or_404(Author, pk=foreign_author_id)
            try:
                follow_request = FollowRequest.objects.get(sender=follower, receiver=followee)
            except FollowRequest.DoesNotExist:
                error_message = 'matching follow request does not exist; you need to create a follow request before '\
                    'you can accept one'
                return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                with transaction.atomic():
                    follow_request_accepted = Follow.objects.create(follower=follower, followee=followee)
                    follow_request.delete()
                
                # TODO: return the serialized follow_request_accepted as response
                return Response({'message': 'OK'}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'message': 'follower already exists'}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, author_id, foreign_author_id):
        serializer = RemoveFollowerSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: for project part 2; follower could be a remote author;
            follow = get_object_or_404(Follow, follower=foreign_author_id, followee=author_id)
            follow.delete()
            return Response({'message': 'follower removed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InboxView(APIView, PaginationHandlerMixin):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsRemotePostOnly]
    pagination_class = BasicPagination
    
    def get_serializer(self, request, queryset):
        return InboxSerializer(queryset, many=True, context={'request': request})

    def get(self, request, author_id):
        """Returns the list of inbox items in the order of newest to oldest"""
        author = get_object_or_404(Author, pk=author_id)
        queryset = author.inbox.order_by('-created_at').all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(
                self.get_serializer(request, page).data
            )
        else:
            serializer = self.get_serializer(request, queryset)
        for data in serializer.data:
            if data['type'] == "like":
                data['post'] = urljoin(data['author']['url'],  f"posts/{data['post']}/")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, author_id):
        if 'type' not in request.data:
            return Response({'message': 'must specify the type of inbox'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data['type'] == 'follow':
            return FollowRequestProcessor(request, author_id).get_response()
        elif request.data['type'] == 'like':
            return LikePostProcessor(request,author_id).get_response()
        else:
            return Response({'message': "unknown 'type'"}, status=status.HTTP_400_BAD_REQUEST)


class NodesView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        queryset = Author.objects.filter(is_remote_user=True).all()
        serializer = NodesListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AddNodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NodeDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]
    
    def delete(self, request, node_id):
        node = get_object_or_404(Author, pk=node_id)
        node.delete()
        return Response({'message': 'node deleted'}, status=status.HTTP_200_OK)
