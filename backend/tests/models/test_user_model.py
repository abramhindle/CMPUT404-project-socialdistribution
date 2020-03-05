from django.contrib.auth import get_user_model
import pytest


User = get_user_model()
test_user_username = "testuser001"
test_user_email = "testemail001@gmail.com"
test_user_password = "ualberta!"
test_user_github_url = "https://github.com/testuser001"


class TestUserModel:

    def test_user_creation(self, test_user):
        assert isinstance(test_user, User)
        assert test_user.username == test_user_username
        assert test_user.email == test_user_email
        assert test_user.check_password(test_user_password)
        assert test_user.githubUrl == test_user_github_url
