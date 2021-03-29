

def get_test_author_fields():
    return {
        'displayName': 'Jon Snow',
        'url': 'www.test_url.com',
        'github': "https://github.com/johnSnow",
        'host': 'localhost:8000'
    }


def get_test_post_fields():
    return {
        'author': 'Jon Snow',
        'title': 'testpost',
        'description': 'I am a test post',
        'source': 'source post id',
        'origin': 'origin post id',
        'visibility': "Public",
        'unlisted': False,
        'contentType': 'text/plain',
        'content': 'Hello, I am a test post',
        'categories': '["Testing"]',
        'commentLink': 'link to comments'
    }
