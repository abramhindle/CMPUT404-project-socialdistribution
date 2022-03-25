from backend.helpers import get_author_list
from .serializers import CommentSerializer


def get_comments(comment_objects):
    comments = CommentSerializer(comment_objects, many=True).data
    authors = get_author_list([comment["author"] for comment in comments])
    for comment in comments:
        found = False
        for author in authors:
            if "id" in author and (comment["author"] in author["id"] or author["id"] in comment["author"]):
                found = True
                comment["author"] = author
                break
        if not found:
            comment["author"] = {"error": "Author Not Found!"}
    return comments
