from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from .models import Author, FollowRequest, Inbox
from .serializers import AuthorSerializer, AuthorRegistrationSerializer, FollowRequestSerializer, SendFollowRequestSerializer
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import status, permissions

class AuthorsView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
        

class AuthorDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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


class FollowRequestsView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, author_id):
        # TODO: for project part 2; will also need to look at the inbox of this author to fetch follow requests
        # received from remote authors
        author = get_object_or_404(Author, pk=author_id)
        serializer = FollowRequestSerializer(author.follow_requests_received.all(), many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


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
            try:
                # https://docs.djangoproject.com/en/4.1/topics/db/transactions/#controlling-transactions-explicitly
                with transaction.atomic():
                    follow_request = FollowRequest.objects.create(sender=sender, receiver=receiver)
                    # update the inbox of the receiver
                    Inbox.objects.create(target_author=receiver, follow_request_sender=sender)

                # TODO: return the new inbox item when we have an Inbox serializer
                return Response({'message': 'OK'}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'message': 'this follow request already exists'}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_response(self):
        return self.response


class InboxView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, author_id):
        if 'type' not in request.data:
            return Response({'message': 'must specify the type of inbox'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data['type'] == 'follow':
            return FollowRequestProcessor(request, author_id).get_response()
        else:
            return Response({'message': "unknown 'type'"}, status=status.HTTP_400_BAD_REQUEST)
