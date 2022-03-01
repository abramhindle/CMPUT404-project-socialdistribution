from collections import OrderedDict
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


def page_number_pagination_class_factory(additional_fields: list[tuple[str, str]]) -> PageNumberPagination:
    """
    Returns a new paginator class that can be used in the `pagination_class` attribute of view sets to
    add additional fields to the root response.

    E.g. to add a `type` field with value 'authors' to the response, the view set should have its `pagination_class` member set to

    ```py
    pagination_class = page_number_pagination_class_factory([('type', 'authors')])
    ```
    """
    class Pagination(PageNumberPagination):
        page_size_query_param = 'size'

        # Override the default JSON fields
        # By Alasdair on Aug 23, 2015 at 19:19
        # https://stackoverflow.com/questions/32170442/remove-count-next-previous-from-response-in-django-rest-framework
        def get_paginated_response(self, data):
            additional_fields.append(('items', data))
            return Response(OrderedDict(additional_fields))
    return Pagination
