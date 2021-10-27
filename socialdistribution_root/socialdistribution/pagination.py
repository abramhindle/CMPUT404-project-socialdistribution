# Pagination implementation guide: https://zoejoyuliao.medium.com/django-rest-framework-add-custom-pagination-c758a4f127fa

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Setting up default page and page size for pagination
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20

class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_query_param = 'page'
    page_size_query_param = 'size'

    # merging of two dictionaries, the second one overrides the first
    def merge_responses(self, dict_info, dict_data):
        return(dict_info.update(dict_data))

    # It takes in a dictionary which ideally has 'data' field with the result of execution,
    # and 'query' fields indicating the function that run.
    # Returns: a response with information about pagination and passed data
    def get_paginated_response(self, dict_data):
        dict_resp = {
            'count': self.page.paginator.count,
            'size': int(self.request.GET.get(self.page_size_query_param, DEFAULT_PAGE_SIZE)),
            'page': int(self.request.GET.get(self.page_query_param, DEFAULT_PAGE)), 
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': dict_data
        }

        # updates dict with the passed in data
        self.merge_responses(dict_resp, dict_data)
        return Response(dict_resp)