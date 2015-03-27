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
            'host': author.get_host(),
            'displayname': author.get_username()
        },
        'friend': {
            'author': {
                'id': remote_author.get_uuid(),
                'host': remote_author.get_host(),
                'displayname': remote_author.get_username(),
                'url': remote_author.get_url()
            }
        }
    }

    nodes = Node.objects.all()

    for node in nodes:
        if node.host in remote_author.get_host():
            try:
                if 'thought-bubble' in node.host:
                    response = requests.post(_tb_friend_request_url(),
                                             headers=_tb_get_headers(author.user.get_username()),
                                             data=json.dumps(request))
                else:
                    response = requests.post('%s/friendrequest' %
                                             node.get_host(),
                                             headers=_get_headers(author.user.get_username()),
                                             data=json.dumps(request))

                print response
                response.raise_for_status()
                return True
            except Exception as e:
                print e.message
                return False

    return False

def get_is_friend(author, remote_author):
    nodes = Node.objects.all()
    for node in nodes:
        if node.host in remote_author.get_host():
            try:
                if 'thought-bubble' in node.host:
                    url = 'http://thought-bubble.herokuapp.com/main/getfriendstatus/?user=%s/%s/' % (author.get_uuid(), remote_author.get_uuid())
                    response = requests.get(url)
                else:
                    response = requests.get('%s/%s/%s' % (node.get_host(), author.get_uuid(), remote_author.get_uuid()))

                response.raise_for_status()

                content = json.load(response.content)
                return content['friends'] == "YES"
            except Exception as e:
                print e.message
                return False

    return False


def _tb_friend_request_url():
    return 'http://thought-bubble.herokuapp.com/main/newfriendrequest/'


def _tb_get_headers(username):
    host = 'host'
    password = 'admin'
    host_url = 'thought-bubble.herokuapp.com'
    authorization = "Basic " + base64.b64encode('%s:%s:%s' % (username, host, password)).replace('\n', '')
    return {'Authorization': authorization, 'Host': host_url}


def _get_headers(username):
    # TODO need to change for the other team
    host = "host"
    password = " admin"
    host_url = 'thought-bubble.herokuapp.com'
    authorization = "Basic " + base64.b64encode('%s:%s:%s' % (username, host, password)).replace('\n', '')
    return {'Authorization': authorization, 'Host': host_url}
