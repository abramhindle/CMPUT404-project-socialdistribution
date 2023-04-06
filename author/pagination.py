from rest_framework.pagination import PageNumberPagination

class InboxSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 9

class AuthorPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 4