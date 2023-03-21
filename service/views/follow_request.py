from django.http import *
from service.models.author import Author
from service.models.follow import Follow
from service.service_constants import *
from django.views import View
import json
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

class AuthorFollowRequests(APIView):
    """ GET an Authors's follow requests -> where they are being followed"""

    http_method_names = ['get']

    # see all author's follow requests -> i.e. who wants to follow them
    def get(self, request, author_id):
        # get all the Follow requests where author is the OBJECT
        author = Author.objects.get(_id=author_id)

        follow_requests = Follow.objects.all().filter(object=author_id)

        requests_json = list()

        for request in list(follow_requests):
            requests_json.append(request.toJSON())

        encoded_json = encode_follow_request_list(requests_json)

        return HttpResponse(json.dumps(encoded_json), content_type=CONTENT_TYPE_JSON)

#TODO: maybe an endpoint to delete a follow request?

def encode_follow_request_list(authors):
    return {
        "type": "Follows",
        "items": authors
    }