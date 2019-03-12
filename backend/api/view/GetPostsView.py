from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Post, AuthorProfile
from ..serializers import PostSerializer, AuthorProfileSerializer

class GetPostsView(generics.GenericAPIView):
    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, authorid):
        author_id = self.kwargs['authorid']
        if(author_id == ""):
            return Response("Error: no author id was specified", status.HTTP_400_BAD_REQUEST)
        else:
            try:
                author_profile = AuthorProfile.objects.get(id=authorid)
                author_posts = Post.objects.filter(author=author_profile)
                posts = PostSerializer(author_posts, many=True).data
                
                response_data = {
                    "query": "posts",
                    "count": len(posts),
                    "posts": posts
                }

                return Response(response_data, status.HTTP_200_OK)
            except:
                return Response("Error: Author does not exist!", status.HTTP_400_BAD_REQUEST)