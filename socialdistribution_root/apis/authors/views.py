from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views import View
from .dto_models import Author
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt

User = apps.get_model('core', 'User')

# Create your views here.

class author(View):
    def get(self, request: HttpRequest, author_id: str):
        user: User = User.objects.get(pk=author_id)
        if (user):
            host = request.get_host()
            return HttpResponse(Author.from_user(user, host).to_json())
        else:
            return HttpResponseNotFound()

    @csrf_exempt 
    def post(self, request: HttpRequest, author_id: str):
        user: User = User.objects.get(pk=author_id)

        if (user):
            host = request.get_host()
            author = Author.from_body(request.body)
            if (author.get_user_id() != str(user.id)):
                return HttpResponseBadRequest("The id of the author in the body does not match the author_id in the request.")
            
            if (author.type != "author"):
                return HttpResponseBadRequest("Can not change the type of an author")

            user = author.merge_user(user)
            user.save()
            return HttpResponse(Author.from_user(user, host).to_json())
        else:
            return HttpResponseNotFound()

class authors(View):
    def get(self, request: HttpRequest):
        host = request.get_host()
        users = User.objects.all()
        authors = list(map(lambda x: Author.from_user(x, host), users))

        return HttpResponse(Author.list_to_json(authors))