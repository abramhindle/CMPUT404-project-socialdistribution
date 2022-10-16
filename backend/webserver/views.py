from rest_framework.views import APIView
from .models import Author
from .serializers import AuthorSerializer
from rest_framework.response import Response
from rest_framework import status

class AuthorsView(APIView):
    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    # commenting out this post request because we will likely need to add two more new fields
    # username and password to the Author model and we also need to set up a separate serializer
    # for creating authors
    # def post(self,request,*args, **kwargs):
    #     author_data = request.data

    #     new_author = Author.objects.create(displayS_name=author_data["display_name"],profile_image=author_data["profile_image"],github_handle=author_data["github_handle"])

    #     new_author.save()
    #     serializer = AuthorSerializer(new_author)

    #     return Response(serializer.data)
        

class AuthorDetailView(APIView):
    # TODO: handle author not found
    def get(self, request, pk, *args, **kwargs):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    # TODO: handle author not found and set up partial update
    def post(self, request, pk, *args, **kwargs):
        author = Author.objects.get(pk=pk)
        data = {
            "display_name": request.data.get('display_name'),
            "profile_image": request.data.get('profile_image'),
            "github_handle": request.data.get('github_handle')
        }
        
        serializer = AuthorSerializer(instance=author, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
