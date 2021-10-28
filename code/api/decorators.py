from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from socialDistribution.models import Author


def authenticate_request(view_func):
    """
        Restrict API path to only {author_id}
    """
    def wrapper_func(request, author_id, *args, **kwargs):
        # check if user f authenticated
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        author = get_object_or_404(Author, user=request.user)

        # check if user is allowed to view resource
        requestId = str(author.id)
        authorId = str(author_id)
        if requestId != authorId:
            return HttpResponse(status=403)

        return view_func(request, author_id, *args, **kwargs)

    return wrapper_func
