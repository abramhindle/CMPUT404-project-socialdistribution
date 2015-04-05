from django.contrib.auth.models import User
from author.models import Author


def createRemoteUser(displayName, host, uuid):
    display_author = 'remote__' + displayName
    password = User.objects.make_random_password(length=20)
    # The password is irrelevant, since we will never
    # authenticate against a remote author.

    user = User.objects.create_user(username=display_author,
                                    password=password)

    return Author.objects.create(user=user, host=host, uuid=uuid)