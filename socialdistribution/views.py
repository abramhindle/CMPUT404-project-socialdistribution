from typing import Any
from django.urls import reverse_lazy, reverse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from requests import Response

from posts.models import Post
from servers.views.generic.list_view import ServerListView
from servers.models import Server


def root(request: HttpRequest) -> HttpResponse:
    if request.user.is_anonymous:
        return redirect(reverse_lazy('auth_provider:login'))
    return redirect(reverse('stream'))


class StreamView(LoginRequiredMixin, ServerListView):
    model = Post
    paginate_by = 10
    template_name = 'stream.html'

    def get_queryset(self) -> QuerySet[Post]:
        return Post.objects.filter(
            visibility=Post.Visibility.PUBLIC,
            unlisted=False).order_by('-date_published')

    def get_endpoints(self) -> list[str]:
        post_endpoints = []
        for server in Server.objects.all():
            resp = server.get('/authors/')
            authors = resp.json()['items']
            for author in authors:
                author_id = author['id']
                # TODO: Update this to author_url once our groupmates are ready (have the URL field)
                authors_posts = f'/authors/{author_id}/posts'
                post_endpoints.append(authors_posts)
        return post_endpoints

    def serialize(self, response: Response) -> list:
        json_response = response.json()

        def to_internal(representation: dict[str, Any]):
            return {
                'title': representation['title'],
                'description': representation['description'],
                'content_type': representation['contentType'],
                'content': representation['content'],
                'date_published': representation['published'],
                'get_absolute_url': representation['source'],  # TODO: Verify whether this is the correct field
            }

        # TODO: Add ['items'] once our groupmates are ready (have the results nested)
        return [to_internal(post) for post in json_response]
