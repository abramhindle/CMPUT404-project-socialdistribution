import Node

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
        if remote_author.get_host() == node.host:
            try:
                response = requests.post('%s/friendrequest' % node.get_host(),
                                         headers=headers,
                                         data=json.dumps(request))
                response.raise_for_status()
            except Exception as e:
                print e.message
