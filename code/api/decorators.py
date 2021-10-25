from django.http import HttpResponse


def authenticate_request(view_func):
    """
        Restrict API path to only {author_id}
    """
    def wrapper_func(request, author_id, *args, **kwargs):
        # check is user is authenticated
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        # check is user is allowed to view resource
        request_id = str(request.user.id)
        author_id = str(author_id)
        if request_id != author_id:
            return HttpResponse(status=403)

        return view_func(request, author_id, *args, **kwargs)

    return wrapper_func
