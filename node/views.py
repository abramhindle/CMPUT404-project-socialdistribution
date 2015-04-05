from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests

from author.models import FriendRequest, Author
from post.models import Post
import post.utils as post_utils
import node.utils as utils
import author.utils as author_utils

import json

from socialdistribution.settings import LOCAL_HOST

AUTHOR = "author"
POST = "post"


@csrf_exempt
def public_posts(request, post_id=None):
    """Return all posts marked as public on the server.
    If a post_id is specified, only return a single post with the provided id.
    """
    if request.user.is_authenticated():
        if request.method == 'GET':
            try:
                response = utils._get_posts(request, post_id, POST)

                return HttpResponse(json.dumps(response),
                                    content_type='application/json',
                                    status=200)
            except Exception as e:
                return HttpResponse(e.message,
                                    content_type='text/plain',
                                    status=500)

        elif request.method == 'POST' or request.method == 'PUT':
            try:
                post_data = json.loads(request.body)
                response = post_utils.updatePost(post_data)

                return HttpResponse(json.dumps(response),
                                    content_type='application/json',
                                    status=200)
            except Exception as e:
                return HttpResponse(e.message,
                                    content_type='text/plain',
                                    status=500)

    return HttpResponse(status=403)


@csrf_exempt
def posts(request, author_id=None):
    """Return the posts that are visible to the current authenticated user.
    If author id is specified, only posts for the specified author will be
    returned.
    """

    if request.user.is_authenticated():
        if request.method == 'GET':
            try:
                response = utils._get_posts(request, author_id, AUTHOR)
            except Exception as e:
                return HttpResponse(e.message,
                                    content_type='text/plain',
                                    status=500)
            return HttpResponse(json.dumps(response), content_type='application/json')

    return HttpResponse(status=403)

def authors(request):
    """
    Returns a list of author currently registered on the server in format of
    {
        'authors':[
            {
                'id': author.uuid
                'displayName: author.username
                'host': author.host
                'url' author.url
            }
        ]
    }
    :return: list of authors
    """
    if request.method == 'GET':
        try:
            authors = Author.objects.all()
            author_list = []

            for author in authors:
                author_list.append(author.get_json_obj())

            return HttpResponse(json.dumps({'authors':author_list}), content_type='application/json')
        except Exception as e:
            return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)

    return HttpResponse(status=405)


@csrf_exempt
def author(request, author_id):
    """
    Returns an author with author ID
    :param author_id: id of the author
    :return: error if no author is found or something else occured
    """
    if request.method == 'GET':
        try:
            author = Author.objects.filter(uuid=author_id)

            if len(author) > 0:
                # We're only expecting one author
                author = author[0]
                return HttpResponse(json.dumps(author.get_json_obj()), content_type='application/json')
            else:
                return HttpResponse(status=405)

        except Exception as e:
            return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)

    return HttpResponse(status=405)


@csrf_exempt
def friends(request, user_id):
    """Return whether anyone in the list is a friend

    This expects a POST request with the following content:

    {
        "query": "friends",
        "author": "9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "authors": [
            "7deee0684811f22b384ccb5991b2ca7e78abacde",
            "31cc28a8fbc05787d0470cdbd62ea0474764b0ae",
            "1af17e947f387a2d8c09a807271bd094e8eff077",
            "77cb4f546b280ea905a6fdd99977cd090613994a",
            "11c3783f15f7ade03430303573098f0d4d20797b",
            "bd9ef9619c7241112d2a2b79505f736fc8d7f43e",
            "0169a8ebf3cb3bd7f092603564873e12cce9d4c5",
            "2130905fd0de94c3379e04839cd9f6889ba2b52c",
            "b32c9e0b5fcf85f46b9ce2ba89b2068b57d4641b",
            "fe45075b93d06c833bb25d5a6dfe669cfde3f99d",
            "e28e59a9612c369717f66f53f3e014b341857601",
            "b36e52d6aaee9285220f94fc321407a44e4dc622",
            "584a9739ea459ce4aae5a88827d970196fb27769",
            "96b3b5a70cd9591c73760bd8669aa5bd7cc689c5",
            "6465678d0a409b96829fd64d0894132966e97eee",
            "695c780ea2815bc94c54782f5046dfa4e325f875",
            "8743f7511a1a569e4e9dacbb25e27395629ba5c0",
            "539b65f2d76d0327dc45bf6354cda535d6f8ed02",
            "c55670261253c5ce25e22b47a34629dd15e819d4"
        ]
    }

    This responds with the following JSON:
    {
        "query": "friends",
        "author": "9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "friends": [
            "7deee0684811f22b384ccb5991b2ca7e78abacde",
            "11c3783f15f7ade03430303573098f0d4d20797b",
        ]
    }
    """
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)

            uuid = request_data['author']
            author = Author.objects.filter(uuid=uuid)

            if len(author) > 0:
                # We're only expecting one author
                author = author[0]

                friends = FriendRequest.get_friends(author)
                uuids = [friend.uuid for friend in friends]
                friends = list(set(uuids) & set(request_data['authors']))

                response = {
                    'query': 'friends',
                    'author': author.uuid,
                    'friends': friends
                }

                return HttpResponse(json.dumps(response),
                                    content_type='application/json',
                                    status=200)
            else:
                return HttpResponse(status=404)
        except Exception as e:
            return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)
    else:
        return HttpResponse(status=405)


@csrf_exempt
def is_friend(request, user_id1, user_id2):
    """Return whether the provided two users are friends.

    This responds with a JSON of the following content:

    {
        "query": "friends",
        "authors": [
            "9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "8d919f29c12e8f97bcbbd34cc908f19ab9496989"
        ],
        # or NO
        "friends":"YES"
    }
    """
    if request.method == 'GET':
        try:
            response = {
                'query': 'friends',
                'authors': [
                    user_id1,
                    user_id2
                ],
                'friends': 'NO'
            }

            author1 = Author.objects.filter(uuid=user_id1)
            author2 = Author.objects.filter(uuid=user_id2)

            if len(author1) > 0 and len(author2) > 0:
                # We're only expecting one author
                author1 = author1[0]
                author2 = author2[0]

                status = FriendRequest.is_friend(author1, author2)
                if status:
                    response['friends'] = 'YES'

                return HttpResponse(json.dumps(response),
                                    content_type='application/json',
                                    status=200)
            else:
                return HttpResponse(status=404)
        except Exception as e:
            return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)
    else:
        return HttpResponse(status=405)


@csrf_exempt
def friend_request(request):
    """Makes a friend request.

    This expects a POST request with the following JSON as the content:

    {
        "query": "friendrequest",
        "author": {
            "id": "8d919f29c12e8f97bcbbd34cc908f19ab9496989",
            "host": "http://127.0.0.1:5454/",
            "displayname": "Greg"
        },
        "friend": {
            "id":"9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "host":"http://127.0.0.1:5454/",
            "displayname":"Lara",
            "url":"http://127.0.0.1:5454/author/
                   9de17f29c12e8f97bcbbd34cc908f1baba40658e"
        }
    }

    If all is well, this responds with a 200 OK.
    """
    if request.method == 'POST':
        try:
            try:
                request_data = json.loads(request.body)

                uuid_author = request_data['author']['id']
                uuid_friend = request_data['friend']['id']
                host_author = request_data['author']['host']
                host_friend = request_data['friend']['host']
                display_author = request_data['author']['displayname']
            except Exception as e:
                return HttpResponse('Bad JSON format: %s' % e.message,
                                    content_type='text/plain',
                                    status=400)

            author = Author.objects.filter(uuid=uuid_author)
            friend = Author.objects.filter(uuid=uuid_friend)

            if len(friend) == 0:
                return HttpResponse('The friend uuid must exist on our server',
                                    content_type='text/plain',
                                    status=400)

            if len(author) == 0:
                # We need to create this author, since it doesn't currently
                # exist.
                try:
                    author = author_utils.createRemoteUser(displayName=display_author,
                                                           host=host_author,
                                                           uuid=uuid_author)
                except Exception as e:
                    return HttpResponse(e.message,
                                        content_type='text/plain',
                                        status=500)

            author = author[0]
            friend = friend[0]

            if friend.host != LOCAL_HOST:
                return HttpResponse('The friend must be a user on our server',
                                    content_type='text/plain',
                                    status=400)

            if FriendRequest.make_request(author, friend):
                return HttpResponse(status=200)
            else:
                return HttpResponse('Could not make friend request for '
                                    'author %s at %s and friend %s at %s. '
                                    'The friend request has already been '
                                    'made.'
                                    % (uuid_author, host_author,
                                       uuid_friend, host_friend),
                                    content_type='text/plain',
                                    status=500)
        except Exception as e:
            return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)
    else:
        return HttpResponse(status=405)


def get_post(request, post_id):
    if request.method == 'GET':
        try:
            query_data = json.load(request.body)
            author_id = query_data['author']['id']
            author_host = query_data['author']['host']
            friends = query_data['friends']

            post = Post.objects.get(guid=post_id)

            for friend in friends:
                friend_check = requests.get(author_host + "friends/" + author_id + "/" + friend)
                if friend_check.status_code == 200:
                    friend_check_data = json.load(friend_check.content)
                    if friend_check_data['friends'] == "YES":
                        friend_obj = utils.getRemoteUserHost(friend)
                        if friend_obj is not None:
                            get_friend_host = request.get(friend_obj.host + "author/" + friend)
                            if get_friend_host.status_code == 200:
                                friend_data = json.load(get_friend_host.content)
                                foaf_check_req_host = request.get(
                                    friend_data['host'] + "friends/" + friend + "/" + author_id)
                                foaf_check_local_host = request.get(
                                    friend_data['host'] + "friends/" + friend + "/" + post.author.uuid)
                                if foaf_check_req_host.status_code == 200 and foaf_check_local_host.status_code == 200:
                                    foaf_check_req_host_data = json.load(foaf_check_req_host.content)
                                    foaf_check_local_host_data = json.load(foaf_check_local_host.content)
                                    if (foaf_check_req_host_data['friends'] == "YES" and
                                                foaf_check_local_host_data['friends'] == "YES"):
                                        return HttpResponse(json.dumps(post_utils.get_post_json(post)),
                                                            content_type='application/json')
                        else:
                            HttpResponse(status=405)

        except Exception as e:
            return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)

    return HttpResponse(status=405)

@csrf_exempt
def foafResponse(request, user_id):
    """
    This responds with the following JSON:
    {
        "query": "friends",
        "author": "9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "friends": [
            "7deee0684811f22b384ccb5991b2ca7e78abacde",
            "11c3783f15f7ade03430303573098f0d4d20797b",
        ]
    }
    """
    if request.method == 'POST':
        try:
            #author = Author.objects.filter(uuid=user_id)
            request_data= json.loads(request.body)
            author = request_data["author"]
            if len(author[0])>0:
                #uuid = request_data['author']
                friends=[]

                for i in request_data["authors"]:
                    if FriendRequest.is_friend(i, author):
                        friends.append(i)

                friends = list(set(friends) & set(request_data["authors"]))
                response = {'query': 'friends','author': author,'friends': friends}

                return HttpResponse(json.dumps(response),
                                    content_type='application/json',
                                    status=200)
            else:
                return HttpResponse(status=404)
        except Exception as e:
            return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)
    else:
        return HttpResponse(status=405)

