from sys import stderr
from typing import Any, Dict, Callable
from requests import Response
from django.views.generic import ListView
from django.core.exceptions import ImproperlyConfigured

from servers.models import Server


class ServerListView(ListView):
    # Override this property to return the path to the resource on the other servers
    endpoint = None

    # Override this method to return the list of objects to append
    serialize: Callable[[Response], list] = None

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        if self.serialize is None:
            raise ImproperlyConfigured(
                "No serializer was given"
            )

        context = super().get_context_data(**kwargs)
        context['object_list'] = [obj for obj in context['object_list']]

        for (server, endpoints) in self.get_server_to_endpoints_mapping():
            for endpoint in endpoints:
                try:
                    resp = server.get(endpoint)
                    context['object_list'] += self.serialize(resp)
                except Exception as err:
                    print(f'Could not serialize {endpoint}, err: {err.with_traceback(None)}', file=stderr)
        return context

    # Override this method if there are multiple endpoints to fetch
    def get_server_to_endpoints_mapping(self) -> list[tuple[Server, list[str]]]:
        if self.endpoint is None:
            raise ImproperlyConfigured(
                "No endpoint configured for multi resource list"
            )
        return [(server, [self.endpoint]) for server in Server.objects.all()]
