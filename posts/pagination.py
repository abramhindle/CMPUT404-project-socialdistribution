from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# custom pagination class to mimic example json
# override the response so that ours follows format, only used for comments and posts
class CustomPagination(PageNumberPagination):
	def get_paginated_response(self, data, query):
		response = {"query" : query,
					"count": self.page.paginator.count}

		if self.get_next_link():
			response["next"] = self.get_next_link()

		if self.get_previous_link():
			response["previous"] = self.get_next_link()

		response[query] = data

		return Response(response)