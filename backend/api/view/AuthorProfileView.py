from rest_framework import generics
from rest_framework import authentication, permissions, status
from ..serializers import UserSerializer, AuthorProfileSerializer
from rest_framework.response import Response
from ..models import AuthorProfile


class AuthorProfileView(generics.GenericAPIView):
    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = AuthorProfileSerializer(data=request.data, context={"request": self.request})

        if (serializer.is_valid(raise_exception=True)):
            httpStatus = status.HTTP_200_OK
            return Response(serializer.data, httpStatus)
        else:
            httpStatus = status.HTTP_400_BAD_REQUEST
            return Response(serializer.errors, httpStatus)

    def get(self, request, uid):
        authorId = self.kwargs['uid']
        query_set = AuthorProfile.objects.filter(id=authorId)
        
        if (len(query_set) == 1):
            response_data = AuthorProfileSerializer(query_set[0]).data
            return Response(response_data, status.HTTP_200_OK)
        else:
            return Response("Author does not exist", status.HTTP_400_BAD_REQUEST)
