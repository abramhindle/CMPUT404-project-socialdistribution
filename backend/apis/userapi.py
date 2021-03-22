from ..serializers import UserSerializer

from rest_framework import generics
from rest_framework import permissions

class UserAPI(generics.RetrieveAPIView):

	permission_classes = [
		permissions.IsAuthenticated,
	]

	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user