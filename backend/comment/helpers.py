import json
from backend.helpers import get_author
from .models import Comment
from .serializers import CommentSerializer
from likes.serializers import LikesSerializer
from backend.DjangoConnectionThreadPoolExecutor import DjangoConnectionThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor


def get_comments(comment_objects):
    comments = CommentSerializer(comment_objects, many=True).data
    with DjangoConnectionThreadPoolExecutor(max_workers=1) as executor:
        future = executor.map(lambda x: get_author(x["author"]), comments)
    items = []
    for comment, author in zip(comments, future):
        item = dict(**comment)
        item["author"] = author
        items.append(item)
    return items
