import json
from backend.helpers import get_author
from likes.serializers import LikesSerializer
from concurrent.futures import ThreadPoolExecutor
from backend.DjangoConnectionThreadPoolExecutor import DjangoConnectionThreadPoolExecutor


def get_likes_helper(like_objects):
    likes = json.loads(json.dumps(LikesSerializer(like_objects, many=True).data))
    with DjangoConnectionThreadPoolExecutor(max_workers=1) as executor:
        future = executor.map(lambda x: get_author(x["author"]), likes)
    items = []
    for like, author in zip(likes, future):
        item = dict(**like)
        item["author"] = author
        items.append(item)
    return items


def get_liked(like_objects):
    return {"type": "liked", "items": get_likes_helper(like_objects)}


def get_likes(like_objects):
    return {"type": "likes", "items": get_likes_helper(like_objects)}
