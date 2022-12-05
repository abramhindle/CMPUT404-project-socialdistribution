from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param
from rest_framework import permissions
from urllib.parse import urlparse
import uuid

class BasicPagination(PageNumberPagination):
    page_size_query_param = 'size'
    
    # overrides this method from the base class so that the page query parameter on the first
    # page is not removed
    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        # if page_number == 1:
        #     return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)


# Reference: https://medium.com/@fk26541598fk/django-rest-framework-apiview-implementation-pagination-mixin-c00c34da8ac2
# Date Accessed: 2022/10/23
# Owner: Frank Liao
class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None or self.request.query_params.get(self.paginator.page_query_param, None) is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)
    
    def get_pagination_string(self):
        s = ""
        if self.request.query_params.get(self.paginator.page_query_param, None) is not None:
            s += f"/?page={self.request.query_params.get(self.paginator.page_query_param)}"
            if self.request.query_params.get(self.paginator.page_size_query_param, None) is not None:
                s += f"&size={self.request.query_params.get(self.paginator.page_size_query_param)}"
        return s

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class IsRemotePostOnly(permissions.IsAuthenticated):
    """
        Local authors and admins are permitted for all requests
        Remote requests are only permitted if they are POST requests
    """
    def has_permission(self, request, view):
        permitted = super().has_permission(request, view)
        if not permitted:
            return False
        if not request.user.is_remote_user:
            return permitted
        
        if request.method == 'POST':
            return True
        return False

class IsRemoteGetOnly(permissions.IsAuthenticated):
    """
        Local authors and admins are permitted for all requests
        Remote requests are only permitted if they are GET requests
    """
    def has_permission(self, request, view):
        permitted = super().has_permission(request, view)
        if not permitted:
            return False
        if not request.user.is_remote_user:
            return permitted
        
        if request.method == 'GET':
            return True
        return False

def is_remote_request(request):
    if not request.user.is_authenticated:
        # if the user is not authenticated, then it cannot be specifically a remote request
        return False
    return request.user.is_remote_user

def join_urls(*urls, ends_with_slash=False):
    url = '/'.join([url.strip('/') for url in urls])
    return url + "/" if ends_with_slash else url

def get_host_from_absolute_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.hostname}/"

def get_author_id_from_url(url):
    id_section = url.split("authors")[1]
    return id_section.split("/")[1].strip("/")

def get_post_id_from_url(url):
    if "posts" not in url:
        return url
    id_section = url.split("posts")[1]
    return id_section.split("/")[1].strip("/")

def get_comment_id_from_url(url):
    if "comments" not in url:
        return url
    id_section = url.split("comments")[1]
    return id_section.split("/")[1].strip("/")

def format_uuid_without_dashes(id: uuid.UUID):
    if isinstance(id, str):
        return id.replace("-", "")
    try:
        return id.hex
    except Exception:
        return id
