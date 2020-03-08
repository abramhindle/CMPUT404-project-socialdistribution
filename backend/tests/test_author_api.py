from django.contrib.auth import get_user_model
from backend.models import User, Friend, Host

import pytest


@pytest.mark.django_db
class TestAuthorAPI:

    def test_get_profile_by_author_id(self, client, test_user, friend_user):
        test_author_id = test_user.id
        Friend.objects.create(
            fromUser=test_user, toUser=friend_user[0])
        Friend.objects.create(
            fromUser=test_user, toUser=friend_user[1])

        response = client.get('/author/{}/'.format(test_author_id))
        assert response.status_code == 200

        assert response.data["id"] == test_user.get_full_user_id()

        assert response.data["displayName"] == test_user.username
        assert response.data["host"] is not None
        assert response.data["url"] == test_user.get_full_user_id()
        assert response.data["Friends"] is not None

        assert response.data["Friends"][0]["id"] == friend_user[0].get_full_user_id(
        )
        assert response.data["Friends"][1]["id"] == friend_user[1].get_full_user_id(
        )

    def test_get_friends(self, client, test_user, friend_user):
        Friend.objects.create(
            fromUser=test_user, toUser=friend_user[0])
        Friend.objects.create(
            fromUser=test_user, toUser=friend_user[1])
        test_auth_id = test_user.id

        response = client.get('/author/{}/friends'.format(test_auth_id))

        assert response.status_code == 200
        assert response.data["query"] == "friends"
        assert response.data["Author"] is not None
        assert response.data["Author"][0] == friend_user[0].get_full_user_id()
        assert response.data["Author"][1] == friend_user[1].get_full_user_id()
