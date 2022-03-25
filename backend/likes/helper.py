import json
from backend.helpers import get_author, get_author_list
from likes.serializers import LikesSerializer
from django import db
from concurrent.futures import ThreadPoolExecutor
from backend.DjangoConnectionThreadPoolExecutor import DjangoConnectionThreadPoolExecutor


def get_likes_helper(like_objects):
    likes = json.loads(json.dumps(LikesSerializer(like_objects, many=True).data))
    authors = get_author([like["author"] for like in likes])
    for like in likes:
        found = False
        for author in authors:
            if "id" in author and (like["author"] in author["id"] or author["id"] in like["author"]):
                found = True
                like["author"] = author
                break
        if not found:
            like["author"] = {"error": "Author Not Found!"}
    return likes


def get_liked(like_objects):
    return {"type": "liked", "items": get_likes_helper(like_objects)}


def get_likes(like_objects):
    return {"type": "likes", "items": get_likes_helper(like_objects)}
