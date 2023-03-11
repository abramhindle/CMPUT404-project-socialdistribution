from rest_framework.pagination import PageNumberPagination

class InboxSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 3