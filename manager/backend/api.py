from django.db.models import query
from .models import Author, Post
from rest_framework import serializers, viewsets, permissions, generics
from rest_framework.response import Response
from .serializers import AuthorSerializer, RegisterSerializer, UserSerializer, PostSerializer, CreateAuthorSerializer
from rest_framework.authtoken.models import Token
import uuid


# Register API
class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = Token.objects.create(user=user)
    print(token)
    userData = UserSerializer(user, context=self.get_serializer_context()).data

    return Response({
      "user": userData
    })

class CreateAuthorAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny
    ]

    

    #serializer_class = CreateAuthorSerializer

    def post(self, request, *args, **kwargs):
        print("TOKEN HERE")
        print(request.META.get('HTTP_AUTHORIZATION'))

        print(request.data)
        author = Author()
        serializer = CreateAuthorSerializer(str(request.META.get('HTTP_AUTHORIZATION')),
                                        displayName=request.data["displayName"],
                                        github=request.data["github"])
        author_id = uuid.uuid4().hex
        host = "127.0.0.1:8000/"

        return Response({
            "token": str(request.META.get('HTTP_AUTHORIZATION')),
            "author_id": author_id,
            "displayName": request.data["displayName"],
            "github" : request.data["github"],
            "host" : host,
            "url" : host + str(author_id)
        })

  



# class CreateAuthorAPI(viewsets.ModelViewSet):
    

#     permission_classes = [
#         permissions.AllowAny
#     ]
    
#     serializer_class = AuthorSerializer

#     def post(self):

#         response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
#         token = Token.objects.get(key=response.data['token'])
#         displayName = Token.objects.get(key=response.data['user'])

#         return Response({
#             "token": token,
#             "displayName": displayName
#         })





# class UserAPI(generics.RetrieveAPIView):
#     permission_classes = [
#         permissions.IsAuthenticated,
#     ]

#     serializer_class = UserSerializer

#     def get_object(self):
#         return self.request.user




class AuthorViewSet(viewsets.ModelViewSet):
    
    queryset = Author.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    serializer_class = AuthorSerializer

    lookup_field = 'id'


# Get Author API
class LoginAPI(viewsets.ModelViewSet):

    #response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)

    print("hello world")
    
    queryset = Author.objects.all()

    print(queryset)

    permission_classes = [
        #permissions.AllowAny
        permissions.AllowAny
    ]
    
    #print(token = Token.objects.get(key=response.data['token']))
    #def get_queryset(self):
    #    return self.request.user.Author.all()

    serializer_class = AuthorSerializer



class PostViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny
    ]

    lookup_field = 'author_id'

    serializer_class = PostSerializer

    queryset = Post.objects.all()

    def list(self, request, author_id=None, id=None, *args, **kwargs):
        if author_id:
            posts = Post.objects.filter(author_id=author_id).order_by('-published')
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, author_id=None, id=None, *args, **kwargs):
        if author_id and id:
            post = Post.objects.filter(id=id)
            serializer = self.get_serializer(post, many=True)
            return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, author_id=None, id=None, *args, **kwargs):
        if author_id and id:
            post = Post.objects.filter(id=id)
            serializer = self.get_serializer(post, many=True)
            deleted_post = serializer.data
            post.delete()
            return Response(deleted_post)
        return super().destroy(request, *args, **kwargs)
