from django.contrib.auth import get_user_model
from backend.models import User, Friend, Host, FriendRequest

import pytest


@pytest.fixture
def test_create_friend_request(self, client, db):
    host = Host.objects.create(
        url="http://www.example.com/index.html"
    )
    test_user = User.objects.create_user(
        username="user01", email="user01@gmail.com", password="cmput404!", githubUrl="https://github.com/user01",
        first_name="user", last_name="testing", host_id=host.id)

    test_user2 = User.objects.create_user(
        username="user02", email="user02@gmail.com", password="cmput404!", githubUrl="https://github.com/user02",
        first_name="user2", last_name="testing2", host_id=host.id)
    post_body_1 = json.dumps({
        "query": "friendrequest",
        "fromUser": test_user,
        "toUser": test_user2
    })
    response = client.post('/friendRequest', data=post_body_1,
                           content_type='application/json', charset='UTF-8')
    assert response.status_code == 200
