from django.contrib.auth import get_user_model
from backend.models import User, Friend, Host, FriendRequest

import json
import pytest

User = get_user_model()
test_user_username = "testuser001"
test_user_email = "testemail001@gmail.com"
test_user_password = "ualberta!"
test_user_github_url = "https://github.com/testuser001"

test_user_username2 = "testuser002"
test_user_email2 = "testemail002@gmail.com"
test_user_password2 = "ualberta!!!"
test_user_github_url2 = "https://github.com/testuser002"


@pytest.mark.django_db
class TestFriend:
    def test_create_friend_request(self, client, test_host):
        test_user2 = User.objects.create_user(
            username=test_user_username2, email=test_user_email2, password=test_user_password2, githubUrl=test_user_github_url2, host=test_host)
        # TODO  test for login - force login and asset response
        test_user = User.objects.create_user(
            username="test_user_username", email=test_user_email, password=test_user_password, githubUrl=test_user_github_url, host=test_host)
        # TODO  Login regularly  and test repsonse

        post_body_1 = json.dumps({
            "query": "friendrequest",
            "author": {
                "id": test_user.fullId,
                "host": test_user.host.url,
                "displayName": test_user.username,
                "url": test_user.fullId
            },
            "friend": {
                "id": test_user2.fullId,
                "host": test_user2.host.url,
                "displayName": test_user2.username,
                "url": test_user2.fullId
            }
        })
        response = client.post('/friendrequest/', data=post_body_1,
                               content_type='application/json', charset='UTF-8')
        assert response.status_code == 201
        # TODO also check if request in the model (filter to check if the data exists)
        client.force_login(test_user2)
        # TODO check response body after
        post_body_2 = json.dumps({
            "query": "friend",
            "toUser": {
                "id": test_user.fullId,
                "host": test_user.host.url,
                "displayName": test_user.username,
                "url": test_user.fullId
            }
        })
        response = client.post('/friend/accept', data=post_body_2,
                               content_type='application/json', charset='UTF-8')
        assert response.status_code == 201
