from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from author.models import FriendRequest, Author
from post.models import Post
from comment.models import Comment


import json

AUTHOR = "author"
POST = "post"


def jdefault(o):
    return o.__dict__


def public_posts(request, post_id=None):
    """Return all posts marked as public on the server.
    If a post_id is specified, only return a single post with the provided id.
    """
    if request.method == 'GET':
        response = _get_posts(request, post_id, POST)
        return HttpResponse(json.dumps(response, indent=4, default=jdefault))
    return HttpResponse(status=400)


def posts(request, author_id=None):
    """Return the posts that are visible to the current authenticated user.

    If author id is specified, only posts for the specified author will be
    returned.

    This responds with the following JSON:
    """
    if request.method == 'GET':
        response = _get_posts(request, author_id, AUTHOR)
        return HttpResponse(json.dumps(response, indent=4, default=jdefault))
    return HttpResponse(status=400)


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

    return HttpResponse(status=400)


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

    return HttpResponse(status=400)


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

    This currently only has support for local authors.
    """
    if request.method == 'POST':
        request_data = json.loads(request.body)

        uuid_author = request_data['author']['id']
        uuid_friend = request_data['friend']['id']

        author = Author.objects.filter(uuid=uuid_author)
        friend = Author.objects.filter(uuid=uuid_friend)

        if len(author) > 0 and len(friend) > 0:
            # We're only expecting one author and one friend
            author = author[0]
            friend = friend[0]

            if FriendRequest.make_request(author, friend):
                return HttpResponse(status=200)

    return HttpResponse(status=400)


def _get_posts(request, id, type):
    user = request.user if request.user.is_authenticated() else None
    if type == AUTHOR:
        if id is not None:
            posts = Post.getVisibleToAuthor(user)
        else:
            posts = Post.getVisibleToAuthor(user, Author.objects.get(uuid=id))

        post_list = _get_post_list(posts)
        return {'posts': post_list}
    else:
        if id is not None:
            posts = Post.getVisibleToAuthor()
            post_list = _get_post_list(posts)
            return {'posts': post_list}
        else:
            post = Post.getPostById(id)
            return {post}


def _get_post_list(posts):
    post_list = []
    for post in posts:
        post_json = post.getJsonObj()

        comment_list = []
        comments = Comment.getCommentsForPost(post)
        for comment in comments:
            comment_list.append(comment.getJsonObj())

        post_json['comments'] = comment_list
        post_list.append(post_json)
    return post_list
