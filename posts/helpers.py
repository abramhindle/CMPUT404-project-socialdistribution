from .models import *
from django.http import Http404
from urllib.parse import urlparse
from .serializers import UserSerializer


def get_user( pk):
        try:
            return User.objects.get(pk=pk)
        except:
            external_servers = Server.objects.all()
            for server in external_servers:
                author = server.get_author_info(pk)
                if author is not None:
                    return author


def get_local_user(pk):
    try:
        return User.objects.get(pk=pk)
    except:
        return None


def parse_id_from_url(url):
    """
    Parses a user id from user urls in the form:
    https://example.com/author/f3be7f78-d878-46c5-8513-e9ef346a759d/
    """
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    path = path.split('/')
    return path[-1]


def get_url(user):
    # TODO: When the serializer is unfucked regarding domain this should use the serializer to spit out the url :)
    # YES this shouldn't be localhost but let's talk when the urls for authors stop being strange
    userSerializer = UserSerializer()
    return userSerializer.get_absolute_url(user)


def get_follow( follower, followee):
    try:
        return Follow.objects.get(followee=followee.url, follower=follower.url)
    except Follow.DoesNotExist:
        return None


def are_friends(user,other):
    followA = get_follow(user,other)
    followB = get_follow(other,user)
    if followA and followB:
        return True
    else:
        return False


def get_friends(user):
    # TODO Update this for node to node
    follows = Follow.objects.filter(follower=user.url).values_list('followee', flat=True)
    followers = Follow.objects.filter(followee=user.url).values_list('follower', flat=True)
    friendIDs = follows.intersection(followers)
    return friendIDs


def are_FOAF(user, other):
    # TODO Update for node to node
    userfriends = get_friends(user)
    otherfriends = get_friends(other)
    bridges = userfriends.intersection(otherfriends)
    return bridges.exists()


def get_friendship_level(user, other):
    # TODO Update for Node to node
    if (are_friends(user, other)):
        return ['FRIENDS', 'FOAF']
    if (are_FOAF(user, other)):
        return ['FOAF']
    return []

def get_follow_request(followee, follower):
    # TODO Update requestor to be from anywhere
    try:
        return FollowRequest.objects.get(requestee=followee, requester=follower)
    except FollowRequest.DoesNotExist:
        return False

def get_follow_request_id(id):
    try:
        return FollowRequest.objects.get(id)
    except FollowRequest.DoesNotExist:
        return False


def has_private_access(user, post):
    try:
        url = get_url(user)
        val = Viewer.objects.get(post=post, url=get_url(user))
        return True
    except Viewer.DoesNotExist:
        return False


def is_local_user(url):
    userHost = urlparse(url).hostname
    return (userHost == SITE_URL)


def visible_to(post, user, direct=False, local=True):
    author = get_user(post.author_id)
    if (user == author):
        return True
    if ((not direct) and post.unlisted):
        return False
    if (post.visibility == "PUBLIC" or post.visibility == "SERVERONLY"):
        return True
    f_level = get_friendship_level(user, author)
    if (post.visibility == "FRIENDS" and not ("FRIENDS" in f_level)):
        return False
    if (post.visibility == "FOAF" and not ("FOAF" in f_level)):
        return False
    if (post.visibility == "PRIVATE" and not has_private_access(user, post)):
        return False
    return True


def get_external_posts(author, requestor):
    external_servers = Server.objects.all()
    for server in external_servers:
        posts = server.get_author_posts(author.id, requestor.id)
        if posts is not None:
            post_models = []
            for post in posts:
                post_model = Post(title=post['title'], content=post['content'], contentType=post['contentType'],
                                  description=post['description'], id=post['id'])
                post_models.append(post_model)
            return post_models
    return []


def get_local_post(post_id):
    try:
        return Post.objects.get(pk=post_id)
    except:
        return None


def get_post(post_id, requestor):
    post = get_local_post(post_id)
    if post is not None:
        return post
    else:
        post = get_external_post(post_id, requestor)
        return post


def get_external_post(post_id, requestor):
    external_servers = Server.objects.all()
    for server in external_servers:
        post = server.get_external_post(post_id, requestor)
        if post is not None:
            author = UserSerializer(data=post['author'])
            author = author.to_user_model()
            post_model = Post(title=post['title'], content=post['content'], contentType=post['contentType'],
                              description=post['description'], id=post['id'], author=author)
            return post_model


def get_local_user_url(user_id):
    return SITE_URL + '{}/'.format(reverse('author', kwargs={'pk': user_id}))


def get_ww_user(user_id):
    try:
        return WWUser.objects.get(user_id=user_id)
    except:
        return None
