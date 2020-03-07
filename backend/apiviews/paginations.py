from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from collections import OrderedDict


class PostPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('query', 'posts'),
            ('count', self.page.paginator.count),
            ('size', self.page_size),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('posts', data)
        ]))
