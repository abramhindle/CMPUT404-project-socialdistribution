from django.http import *
from service.models.author import Author
from service.models.follow import Follow
from service.service_constants import *
from django.views import View
import json
from djongo.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class AuthorFollowRequests(View):
    """ GET an Authors's follow requests -> where they are being followed"""

    http_method_names = ['get']

    # see all author's follow requests -> i.e. who wants to follow them
    def get(self, request, author_id):
        #get all the Follow requests where author is the OBJECT
        author = Author.objects.get(_id = author_id)

        follow_requests = Follow.objects.all().filter(object=author_id)

        requests_json = list()

        for r in list(follow_requests):
            requests_json.append(r.toJSON())

        encoded_json = encode_follow_request_list(requests_json)

        return HttpResponse(json.dumps(encoded_json), content_type = CONTENT_TYPE_JSON)

#TODO: maybe an endpoint to delete a follow request?
@method_decorator(csrf_exempt, name='dispatch')
class FollowRequests(View):
    http_method_names = ['put', 'delete']

    def post(self, request, author_id, foreign_author_id):
        #if request.user.is_authenticated:
        follow_requests = Follow.objects.all().filter(object=author_id)
        if author_id == foreign_author_id:
            return HttpResponseBadRequest() #can't follow yourself!

        author = Author.objects.get(_id = author_id)
        follower = Author.objects.get(_id = foreign_author_id)

        try:
            author.followers.get(_id=foreign_author_id)
        except ObjectDoesNotExist:
            r = Follow()
            r.actor = follower
            r.object = author
            r.save()

            return HttpResponse(status=200)

        return HttpResponse(status=409)

    def delete(self, request, author_id, foreign_author_id):
        follow_requests = Follow.objects.all().filter(object=author_id)
        for r in follow_requests:
            if r.actor._id == foreign_author_id:
                follow_requests.remove(r)
                follow_requests.save()

        return HttpResponse(status=200)


def encode_follow_request_list(authors):
    return {
        "type": "Follows",
        "items": authors
    }