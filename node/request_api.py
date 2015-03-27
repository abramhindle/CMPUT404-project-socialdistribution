from node.models import Node

import json
import requests


def post_friend_request(author, remote_author):
    """Posts a friend request to a remote author from a local author."""
    headers = {'Content-type': 'application/json'}
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
                                             headers=headers,
                                             data=json.dumps(request))
                else:
                    response = requests.post('%s/friendrequest' %
                                             node.get_host(),
                                             headers=headers,
                                             data=json.dumps(request))

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

def get_friends_in_list(author, authors):
    headers = {'Content-type': 'application/json'}
    request = {'query':'friends',
                'author':author.get_uuid,
                "authors":[authors]}

    nodes = Node.objects.all()

    for node in nodes:
        if node.host in remote_author.get_host():
            try: 
                if 'thought-bubble' in node.host:
                    response = requests.post('http://thought-bubble.herokuapp.com/main/checkfriends/?user=%s/' % (author.get_uuid()),
                                            headers=headers,
                                            data=json.dumps(request))
                else:
                    response = requests.post('%s/friends/%S' % (node.get_host(), author.get_uuid())
                                            headers=headers,
                                            data=json.dumps(request))

                content = json.load(response.content)
                return content.get("friends")
            except Exception as e:
                return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)

    return ""

def _tb_friend_request_url():
    return 'http://thought-bubble.herokuapp.com/main/newfriendrequest/'
