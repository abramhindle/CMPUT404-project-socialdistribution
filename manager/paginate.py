from rest_framework.pagination import PageNumberPagination

class ResultsPagination(PageNumberPagination):
	page_size = 50
	page_size_query_param = 'size'
	page_query_param = 'page'