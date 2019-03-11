from django.db import transaction
from rest_framework import generics
from rest_framework import authentication, permissions, status
from ..serializers import AuthorProfileSerializer
from rest_framework.response import Response
from ..models import AuthorProfile


class AuthorProfileView(generics.GenericAPIView):
    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    immutable_keys = ["id", "host"]

    def post(self, request, uid):
        authorId = self.kwargs['uid']

        if(authorId == ""):
            return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)
        
        else:
            try:
                author_to_update = AuthorProfile.objects.get(id=uid)
                if(request.user.authorprofile.id != author_to_update.id):
                    return Response("Error: You do not have permission to edit this profile", status.HTTP_400_BAD_REQUEST)
                else:
                    for key, value in request.data.items():
                        if key not in self.immutable_keys:
                            setattr(author_to_update, key, value)
                        else:
                            return Response("Error: Can't modify field", status.HTTP_400_BAD_REQUEST)

                    author_to_update.save()
                    return Response("Success: Successfully updated profile", status.HTTP_200_OK)
            except:
                return Response("Error: You do not have permission to update", status.HTTP_400_BAD_REQUEST)

    def get(self, request, uid):
        authorId = self.kwargs['uid']
        if(authorId == ""):
            return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)

        tmp = authorId.split("author/")
        if(len(tmp) == 2):
            query_set = AuthorProfile.objects.filter(host=tmp[0], id=tmp[1])
            if (len(query_set) == 1):
                response_data = AuthorProfileSerializer(query_set[0]).data
                return Response(response_data, status.HTTP_200_OK)
            else:
                return Response("Author does not exist", status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Author does not exist2", status.HTTP_400_BAD_REQUEST)
