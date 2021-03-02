def initial_author_field(user):
    return {
        "id": "http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        # the home host of the author
        "host": "http://127.0.0.1:8000/",
        # the display name of the author
        "displayName": "Lara Croft",
        # url to the authors profile
        "url": "http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        # HATEOS url for Github API
        "github": "http://github.com/laracroft",
        "user": user,
    }


def initial_user_field():
    return {
        "username": "username",
        "email": "email@gmail.com",
        "password": "LaraCroft1234",
    }


def initial_post_author_field():
    return {
        "id": "http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        # the home host of the author
        "host": "http://127.0.0.1:8000/",
        # the display name of the author
        "displayName": "Lara Croft",
        # url to the authors profile
        "url": "http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        # HATEOS url for Github API
        "github": "http://github.com/laracroft",
        "username": "username",
    }
