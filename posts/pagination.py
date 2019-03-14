from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# custom pagination class to mimic example json
# override the response so that ours follows format, only used for comments and posts
class CustomPagination(PageNumberPagination):
	page_size_query_param = "size"

	def get_paginated_response(self, data, query):
		response = {"query" : query,
					"count": self.page.paginator.count,
					"size" : self.page_size}

		if self.get_next_link():
			response["next"] = self.get_next_link()

		if self.get_previous_link():
			response["previous"] = self.get_previous_link()

		response[query] = data

		return Response(response)

	def paginate_queryset(self, queryset, request, view=None):
		"""
		Paginate a queryset if required, either returning a
		page object, or `None` if pagination is not configured for this view.
		"""
		page_size = self.get_page_size(request)
		self.page_size = page_size
		if not page_size:
			return None

		paginator = self.django_paginator_class(queryset, page_size)
		page_number = request.query_params.get(self.page_query_param, 1)
		if page_number in self.last_page_strings:
			page_number = paginator.num_pages

		try:
			self.page = paginator.page(page_number)
		except InvalidPage as exc:
			msg = self.invalid_page_message.format(
				page_number=page_number, message=six.text_type(exc)
			)
			raise NotFound(msg)

		if paginator.num_pages > 1 and self.template is not None:
			# The browsable API should display pagination controls.
			self.display_page_controls = True

		self.request = request
		return list(self.page)