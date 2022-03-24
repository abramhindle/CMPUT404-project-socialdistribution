from sys import stderr
from typing import Any, Callable, Optional
from django.views.generic import DetailView
from django.http import Http404
from django.db import models
from requests import get, Response

from servers.models import Server

from posts.models import Post


class ServerDetailView(DetailView):
    # Override this method to map their object to ours
    to_internal: Callable[[Response], Any] = None

    def get_object(self, queryset: Optional[models.query.QuerySet] = None) -> Post:
        servers = Server.objects.all()
        url = self.kwargs['url']
        for server in servers:
            if not url.startswith(server.service_address):
                continue
            # Trim prefix
            resp = server.get(url[len(server.service_address):])
            try:
                return self.to_internal(resp)
            except Exception as err:
                print(f'Failed to internalize {url}, err: {err.with_traceback(None)}', file=stderr)

        raise Http404
