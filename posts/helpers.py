from .models import *
from django.http import Http404
from urllib.parse import urlparse
# need to import this way to avoid circular dependency :(
import posts.serializers
from preferences import preferences
import requests
from rest_framework.response import Response



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

def parse_host_from_url(url):
    """
    parses out host name from a url
    """
    parsed = urlparse(url)
    return parsed.netloc


def get_url(user):
    # TODO: When the serializer is unfucked regarding domain this should use the serializer to spit out the url :)
    # YES this shouldn't be localhost but let's talk when the urls for authors stop being strange
    userSerializer = posts.serializers.UserSerializer()
    return userSerializer.get_absolute_url(user)


def get_follow(follower, followee):
    try:
        return Follow.objects.get(followee=followee.url, follower=follower.url)
    except Follow.DoesNotExist:
        return None


def are_friends(user, other):
    followA = get_follow(user, other)
    followB = get_follow(other, user)
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
    try:
        return WWUser.objects.get(url=url).local
    except:
        return False


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
                                  description=post['description'], id=post['id'], source=post['source'],
                                  origin=post['origin'])
                post_models.append(post_model)
            return post_models
    return []


def post_dict_to_model(post):
    """
    given a dictionary representing a post, this converts the dict to an object
    Assumptions:
        - the key 'author' MUST be defined in 'post'
            - where 'author' is another dictionary representing a user
            - can be local or external
        - id, title, content, contentType, description must also be defined
    Returns:
        - Post object
            - however, note that the Post object will not be saved into the db
    """
    author = posts.serializers.UserSerializer(data=post['author'])
    author = author.to_user_model()
    post_model = Post(title=post['title'], content=post['content'], contentType=post['contentType'],
                      description=post['description'], id=post['id'], author=author, source=post['source'],
                      origin=post['origin'])
    return post_model


def mr_worldwide(requestor, is_proxy_request, visibility="PUBLIC", exclude_servers=[]):
    """
    returns list of worldwide Post objects, with source and origin properly set
    requestor is a user object
    Arguments:
        - is_proxy_request:
            - boolean which describes if this requestor is another server or end user
        - visibility:
            - only posts that have this visibility will be returned
            - other servers should only be sending us PUBLIC posts anyways so this
              is more for clarity than anything
        - exclude_servers:
            - list of servers not to fetch from
            - basically just to avoid cycles but idk if this is how we'll do it
    Return:
        - all_posts : list
            - list of Post objects from every server we are connected to, excluding servers in 'exclude_servers'
    """
    image_types = ['image/png;base64', 'image/jpeg;base64']

    external_servers = Server.objects.exclude(server__in=exclude_servers)
    all_posts = []

    for server in external_servers:
        # TODO: handle case where this returns None, or dont idk
        posts_data = server.get_server_posts(requestor)
        if (posts_data is None):
            continue
        posts_list = posts_data['posts']
        for post_dict in posts_list:
            if (post_dict["visibility"] != visibility):
                # continue to next iteration
                continue
            if (post_dict["contentType"] in image_types):
                # continue to next iteration
                # NOTE: shouldnt need to do this since other api's shouldnt be sending us
                # posts with image content from /posts/ anyways but this is ensures image blobs arent shown
                continue

            post_model = post_dict_to_model(post_dict)
            # NOTE: this might not be accurate, server.server might not be what im expecting
            # what I mean: does server.server also have http proto prefix? ¯\_(ツ)_/¯
            # but whatever frontend wont see source anyways
            new_source = "{}/posts/{}".format(server.server, post_model.id)
            post_model.source = new_source
            all_posts.append(post_model)

    # for post in all_posts:
    #     print(post.title)


    return all_posts


def get_local_post(post_id):
    try:
        return Post.objects.get(pk=post_id)
    except:
        return None


def get_post(post_id, requestor):
    post = get_local_post(post_id)
    if post is not None:
        return post, None
    else:
        post, comments = get_external_post(post_id, requestor)
        return post, comments


def get_external_post(post_id, requestor):
    external_servers = Server.objects.all()
    for server in external_servers:
        post = server.get_external_post(post_id, requestor)
        if post is not None:
            # author = posts.serializers.UserSerializer(data=post['author'])
            # author = author.to_user_model()
            # post_model = Post(title=post['title'], content=post['content'], contentType=post['contentType'],
            #                   description=post['description'], id=post['id'], author=author, source=post['source'],
            #                   origin=post['origin'])
            post_model = post_dict_to_model(post)
            comment_list = []
            for comment in post['comments']:
                # CHeck if paginated
                commenter_wwuser = WWUser.objects.get_or_create(url=comment['author']['url'],
                                                                user_id=comment['author']['url'].split('/author/')[-1])[0]
                comment_model = Comment(comment=comment['comment'])
                comment_model.author = commenter_wwuser
                comment_model.parent_post = post_model
                comment_list.append(comment_model)
            comment_serializer = posts.serializers.CommentSerializer(data=comment_list, many=True)
            comment_serializer.is_valid()
            comment_list = comment_serializer.data
            return post_model, comment_list
        return None, None

def get_local_user_url(user_id):
    return SITE_URL + '{}/'.format(reverse('author', kwargs={'pk': user_id}))


def get_ww_user(user_id):
    try:
        return WWUser.objects.get(user_id=user_id)
    except:
        return None


def get_local_posts(images=True):
    if images:
        return Post.objects.filter(visibility='PUBLIC').order_by("-published")
    else:
        return Post.objects.filter(visibility='PUBLIC').exclude(
            contentType__in=['img/png;base64', 'image/jpeg;base64'])


def get_external_friends(url):
    r = requests.get(url)
    if r.status_code == 200:
        friends = json.loads(r.content.decode('utf-8'))['authors']
        return friends
    return []


def try_get_viewer(post, url):
    try:
        return Viewer.objects.get(post=post, url=url)
    except:
        return False


def get_id_from_url(url):
    if url[-1] == '/':
        url = url[:-1]
    return url.split('/')[-1]
