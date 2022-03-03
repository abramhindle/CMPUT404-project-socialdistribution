from django.urls import reverse_lazy, reverse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView

from posts.models import Post


def root(request: HttpRequest) -> HttpResponse:
    if request.user.is_anonymous:
        return redirect(reverse_lazy('auth_provider:login'))
    return redirect(reverse('stream'))


class StreamView(ListView):
    model = Post
    paginate_by = 100
    template_name = 'stream.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Post.objects.filter(
            visibility=Post.Visibility.PUBLIC,
            unlisted=False).order_by('-date_published')
        return context
