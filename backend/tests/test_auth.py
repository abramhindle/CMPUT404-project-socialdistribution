from backend.models import User
from django.conf import settings

import pytest
import json


@pytest.mark.django_db
def test_signup(client):

    test_user1_username = "testuser001"
    test_user1_email = "testemail001@gmail.com"
    test_user1_password = "ualberta!"

    post_body_1 = json.dumps({
        "username": test_user1_username,
        "email": test_user1_email,
        "password1": test_user1_password,
        "password2": test_user1_password
    })

    response = client.post('/auth/registration/', data=post_body_1,
                           content_type='application/json', charset='UTF-8')
    assert response.status_code == 201

    test_user = User.objects.get(username="testuser001")
    assert test_user.username == test_user1_username
    assert test_user.email == test_user1_email
    assert test_user.host.url == settings.APP_HOST
    assert test_user.check_password(test_user1_password)
    assert test_user.is_active is False
    assert test_user.is_superuser is False
