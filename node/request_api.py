from node.models import Node
import base64
import json
import requests


def post_friend_request(author, remote_author):
    """Posts a friend request to a remote author from a local author."""

    request = {
        'query': 'friendrequest',
        'author': {
            'id': author.get_uuid(),
            'host': 'http://social-distribution.herokuapp.com/api',
            'displayname': author.get_username()
        },
        'friend': {
            'id': remote_author.get_uuid(),
            'host': remote_author.get_host(),
            'displayname': remote_author.get_username(),
            'url': remote_author.get_url()
        }
    }

    print json.dumps(request)

    nodes = Node.objects.all()

    for node in nodes:
        if node.host in remote_author.get_host():
            try:
                if 'thought-bubble' in node.host:
                    response = requests.post('http://thought-bubble.herokuapp.com/main/api/newfriendrequest/',
                                             headers=_tb_get_headers(
                                                 author.user.get_username(),
                                                 True),
                                             data=json.dumps(request))
                else:
                    response = requests.post('http://hindlebook.tamarabyte.com/api/friendrequest',
                                             headers=_hb_get_headers(
                                                 author.user.get_username()),
                                             data=json.dumps(request))
                print response

                response.raise_for_status()
                print 'SUCCESS - friend request posted'
                return True
            except Exception as e:
                return False

    return False


def get_is_friend(author, remote_author):
    nodes = Node.objects.all()
    for node in nodes:
        #if node.host in remote_author.get_host():
        try:
            if 'thought-bubble' in node.host:
                url = 'http://thought-bubble.herokuapp.com/main/api/getfriendstatus/?user=%s/%s/' % (
                            author.get_uuid(), remote_author.get_uuid())
                response = requests.get(
                    url, headers = _tb_get_headers('username'))
                response.raise_for_status()
                content2 = json.loads(response.content)
                print(content2['friends'])
                if content2['friends']=='NO':
                    return False
                return True
                #else:
                #    url = 'http://hindlebook.tamarabyte.com/api/friends/%s/%s' % (author.get_uuid(), remote_author.get_uuid())
                #    response = requests.get(url,
                 #                           auth = ('team6', 'team6'),
                 #                           headers = {'Uuid': uuid})
                 #   response.raise_for_status()
                 #   content2 = json.loads(response.content)
                #    print(content2['friends'])
                 #   return content2['friends']
        except Exception as e:
            print e.message
            return False


def get_friends_in_list(author, authors, uuid):
    """ get the friends from a list of a remote author """
    request = {'query': 'friends',
               'author': author.get_uuid(),
               "authors": [authors]}

    nodes = Node.objects.all()

    for node in nodes:
        if node.host in author.get_host():
            try:
                if 'thought-bubble' in node.host:
                    response = requests.post('http://thought-bubble.herokuapp.com/main/picheckfriends/?user=%s' % (author.get_uuid()),
                                             headers=_tb_get_headers(
                                                 author.user.get_username()),
                                             data=json.dumps(request))
                else:
                    url = 'http://hindlebook.tamarabyte.com/api/friends/%s' % (author.get_uuid())
                    response = requests.get(url,
                                auth = ('team6', 'team6'),
                                headers = {'Uuid': uuid},
                                data = json.dumps(request))

                content = json.load(response.content)
                return content.get("friends")
            except Exception as e:
                return HttpResponse(e.message,
                                    content_type='text/plain',
                                    status=500)

    return ""


def _tb_get_headers(username, omit_auth=False):
    host = 'social-distribution.herokuapp.com'
    password = 'admin'
    host_url = 'thought-bubble.herokuapp.com'
    authorization = "Basic " + \
        base64.b64encode('%s:%s:%s' %
                         ('admin', host, password)).replace('\n', '')

    if omit_auth:
        return {}
    else:
        return {'Authorization': authorization, 'Host': host_url}


def _hb_get_headers(username):
    username = 'team6'
    password = 'team6'
    authorization = "Basic " + \
        base64.b64encode('%s:%s' %
                         (username, password)).replace('\n', '')
    return {'Authorization': authorization, 'Content-Type': 'application/json'}

def foafPost(request,author):
    '''
    {"query":"getpost",
     "id":"9de17f29c12e8f97bcbbd34cc908f1baba40658e",
     "author":{
            "id":"8d919f29c12e8f97bcbbd34cc908f19ab9496989",
            "host":"http://127.0.0.1:5454/",
            "displayname":"Greg"
    },
    "friends":[
            "7deee0684811f22b384ccb5991b2ca7e78abacde",
            "11c3783f15f7ade03430303573098f0d4d20797b",
                ]
    }
    '''
    request_data=json.loads(request.body)


