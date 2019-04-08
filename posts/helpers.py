from .models import *
from urllib.parse import urlparse
from .serializers import UserSerializer

# need to import this way to avoid circular dependency :(
import posts.serializers
import requests



def get_user( pk):
        try:
            return User.objects.get(pk=pk)
        except:
            external_servers = Server.objects.all()
            for server in external_servers:
                author = server.get_author_info(pk)
                if author is not None:
                    return author
            return None


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
    """Takes in two user or WW_user models"""
    try:
        return Follow.objects.get(followee=followee, follower=follower)
    except Follow.DoesNotExist:
        return None


def are_friends(ww_user, ww_author):
    # on the local side we must check if the author follows the user
    local_friendship = get_follow(follower=ww_author, followee=ww_user)
    other_friendship = False
    if local_friendship:
        if ww_author.local and ww_user.local:
            # local friendship! ezpz
            other_friendship = get_follow(follower=ww_user, followee=ww_author)
        else:
            # external friendship, hard and sad :(
            friends = get_external_friends(ww_user)
            if ww_author in friends:
                other_friendship = True
    return local_friendship and other_friendship


def get_friends(ww_user):
    """Change to WW_user"""
    follows = Follow.objects.filter(follower=ww_user).values_list('followee', flat=True)
    return follows


def are_FOAF(ww_user, ww_other):
    """Needs WW Users"""
    # TODO Update for node to node
    if ww_other.local:
        userfriends = get_friends(ww_user)
        otherfriends = get_friends(ww_other)
        bridges = userfriends.intersection(otherfriends)
        return bridges.exists()
    else:
        return get_ext_foaf(ww_other,ww_user)


def get_friendship_level(ww_user, ww_author):
    # TODO Update for Node to node
    if are_friends(ww_user, ww_author):
        return ['FRIENDS', 'FOAF']
    if are_FOAF(ww_user, ww_author):
        return ['FOAF']
    return []

def get_follow_request(requestee, requester):
    try:
        return FollowRequest.objects.get(requestee=requestee, requester=requester)
    except FollowRequest.DoesNotExist:
        return False

def get_follow_request_id(id):
    try:
        return FollowRequest.objects.get(id)
    except FollowRequest.DoesNotExist:
        return False


def has_private_access(ww_user, post):
    try:
        val = Viewer.objects.get(post=post, url=ww_user.url)
        return True
    except Viewer.DoesNotExist:
        return False


def is_local_user(url):
    try:
        return WWUser.objects.get(url=url).local
    except:
        return False


def visible_to(post, ww_user, direct=False, local=True):
    author = get_user(post.author_id)
    ww_author = get_ww_user(user_id=author.id)
    if (ww_user.user_id == ww_author.user_id):
        return True
    if ((not direct) and post.unlisted):
        return False
    if (post.visibility == "PUBLIC" or (post.visibility == "SERVERONLY" and local)):
        return True
    friends = are_friends(ww_user,ww_author)
    if (post.visibility == "FRIENDS" and not friends):
        return False
    if friends:
        foaf = True
    else:
        foaf = are_FOAF(ww_user,ww_author)
    if (post.visibility == "FOAF" and not foaf):
        return False
    if (post.visibility == "PRIVATE" and not has_private_access(ww_user, post)):
        return False
    return True


def get_external_author_posts(author, requestor):
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


def mr_worldwide(requestor, is_proxy_request, visibility=["PUBLIC"], exclude_servers=[]):
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

    external_servers = Server.objects.exclude(server__in=exclude_servers)
    all_posts = []

    for server in external_servers:
        # TODO: handle case where this returns None, or dont idk
        posts_data = server.get_server_posts(requestor)
        if (posts_data is None):
            continue
        posts_list = posts_data['posts']
        for post_dict in posts_list:
            if not (post_dict["visibility"] in visibility):
                # continue to next iteration
                continue

            post_model = post_dict_to_model(post_dict)
            # NOTE: this might not be accurate, server.server might not be what im expecting
            # what I mean: does server.server also have http proto prefix? ¯\_(ツ)_/¯
            # but whatever frontend wont see source anyways
            new_source = "{}/posts/{}".format(server.api, post_model.id)
            post_model.source = new_source
            all_posts.append(post_model)

    # for post in all_posts:
    #     print(post.title)

    return all_posts

def get_external_feed(requestor):
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
    ww_user = get_ww_user(requestor.id)
    external_servers = Server.objects.all()
    all_posts = []

    for server in external_servers:
        # TODO: handle case where this returns None, or dont idk
        posts_data = server.get_ext_feed(requestor)
        if (posts_data is None):
            continue
        posts_list = posts_data['posts']
        for post_dict in posts_list:
            if (post_dict["visibility"] == "FRIENDS"):
                # continue to next iteration
                try:
                    # Ghetto way to check if the user is following the user locally
                    ww_author = WWUser.objects.get(url=post_dict["author"]["url"])
                    follow =Follow.objects.get(follower=ww_user,followee=post_dict["author"]["url"])
                except:
                    continue

            post_model = post_dict_to_model(post_dict)
            # NOTE: this might not be accurate, server.server might not be what im expecting
            # what I mean: does server.server also have http proto prefix? ¯\_(ツ)_/¯
            # but whatever frontend wont see source anyways
            new_source = "{}/posts/{}".format(server.api, post_model.id)
            post_model.source = new_source
            all_posts.append(post_model)

    # for post in all_posts:
    #     print(post.title)

    return all_posts

def get_local_post(post_id):
    try:
        return Post.objects.get(id=post_id)
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
            post_model = post_dict_to_model(post)
            comment_list = []
            for comment in post['comments']:
                # CHeck if paginated
                user_id = get_id_from_url(comment['author']['url'])
                try:
                    commenter_wwuser = WWUser.objects.get(user_id=user_id)
                except:
                    commenter_wwuser = WWUser.objects.get_or_create( url=comment['author']['url'],user_id=user_id)[0]
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


def get_or_create_ww_user(user):
    ww_user = get_ww_user(user_id=user.id)
    if ww_user:
        return ww_user
    url = str(user.host) + 'author/' + str(user.id)
    local = user.host == SITE_URL
    ww_user = WWUser.objects.create(user_id=user.id, url=url, local=local)
    ww_user.save()
    return ww_user

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


def in_user_friends(user,author):
    # we pass in two user objects

    external_friends = get_external_friends(friend_check_url)
    author_serialized = UserSerializer(instance=author)


def get_id_from_url(url):
    if url[-1] == '/':
        url = url[:-1]
    return url.split('/')[-1]


def get_or_create_external_header(external_header):
    user_id = external_header.split('/author/')[1]
    i_hate_michaels_group = external_header.split('/author/')[0]
    if i_hate_michaels_group == 'https://cmput404-front-test.herokuapp.com':
        url = 'https://cmput404-front-test.herokuapp.com/api/author/{}'.format(user_id)
        # TODO Update for deployment
    else:
        url = external_header
    if user_id[-1] == '/':
        user_id = user_id[:-1]
    return WWUser.objects.get_or_create(user_id=user_id, url=url)[0]

def get_ext_foaf(local_user,ext_user):
    # Returns a boolean indicating whether these users are foaf
    # THESE ARE WW USERS
    local_follows = Follow.objects.filter(follower=local_user).values_list("followee")
    local_follows = [x for x in local_follows]
    if local_follows:
        url = ext_user.url + ("/" if (ext_user.url[-1]!="/") else "") + "friends/"
        ext_friends = get_external_friends(url)
        for follow in local_follows:
            if follow[0] in ext_friends:
                return True
    else:
        return False



