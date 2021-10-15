from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class PageSizePagination(PageNumberPagination):
    page_size_query_param = 'size' # use query param 'size'

    def __init__(self):
        super().__init__()
        self.key = 'items'

    def get_paginated_response(self, data):
        response = {}
        # include the response type if it exist
        if hasattr(self, 'type'):
            response['type'] = self.type
        response.update({
            'page': int(self.get_page_number(request=self.request, paginator=self.page.paginator)),
            'size': int(self.get_page_size(request=self.request)),
            self.key: data
        })
        return Response(response) 
