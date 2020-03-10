from django.utils.timezone import make_aware
from profiles.models import Author
from posts.models import Post, Comment
from datetime import datetime
import dateutil.parser  # pip install python-dateutil


def post_to_dict(post):
    comments = Comment.objects.filter(post=post)

    return {
        "title" : post.title,
        "source" : "POST HAS NO ATTRIBUTE SOURCE",
        "origin" : "POST HAS NO ATTRIBUTE ORIGIN",
        "description" : post.description,
        "contentType" : post.content_type,
        "content" : "POST HAS NO ATTRIBUTE CONTENT",
        "author" : author_to_dict(post.author),
        "categories":["web","tutorial"],
        "count" : comments.count(),
        "size" : "IMPLEMENT PAGINATION",
        "next" : "IMPLEMENT PAGINATION",
        "comments" : [comment_to_dict(comment) for comment in comments],
        "published" : post.published.isoformat(),
        "id" : post.id,
        "visibility" : post.visibility,
        "visibleTo" : post.visibileTo,
        "unlisted" : post.unlisted
    }

def author_to_dict(author):
    return {
        "id" : author.id,
        "url" : author.url,
        "host" : author.host,
        "displayName" : author.displayName,
        "github" : author.github
    }

def comment_to_dict(comment):
    return {
        "author" : author_to_dict(comment.author),
        "comment" : comment.comment,
        "contentType" : comment.content_type,
        "published" : comment.published.isoformat(),
        "id" : comment.id    
    }

def is_valid_post(post_dict):
    fields = [
        # field, type, required
        ("title", str, True), 
        ("description", str, True), 
        ("contentType", str, True), 
        ("content", str, True), 
        ("categories", list, True), 
        ("visibility", str, True), 
        ("unlisted", bool, True),
        ("published", str, False)
    ]

    post_fields = post_dict.keys()

    # general validation
    for field, field_type, required in fields:
        # missing a required field
        if required and field not in post_fields:
            return False
        if field in post_fields:
            # wrong type for field
            if not isinstance(post_dict[field], field_type):
                return False

    # make sure if they included a timestamp, it's a valid timestamp
    if "published" in post_fields:
        try:
            datetime = dateutil.parser.isoparse(post_dict["published"])
        except:
            return False

    return True

def insert_post(post_dict):
    # for now just get a dummy author
    author = Author.objects.all()[0]

    post_fields = post_dict.keys()

    if "published" in post_fields:
        post_datetime = make_aware(dateutil.parser.isoparse(post_dict["published"]))
    else:
        post_datetime = datetime.utcnow()

    post = Post(
        title=post_dict["title"],
        description=post_dict["description"],
        categories=post_dict["categories"],
        published=post_datetime,
        author=author,
        visibility=post_dict["visibility"],
        unlisted=post_dict["unlisted"],
        content_type=post_dict["contentType"]
    )

    post.save()

    return post

def update_post(post, new_post_dict):
    new_fields = new_post_dict.keys()

    if "title" in new_fields:
        post.title = new_post_dict["title"]
    if "description" in new_fields:
        post.description = new_post_dict["description"]
    if "categories" in new_fields:
        post.categories = new_post_dict["categories"]
    if "published" in new_fields:
        post_datetime = make_aware(dateutil.parser.isoparse(new_post_dict["published"]))
        post.published = post_datetime
    if "visibility" in new_fields:
        post.visibility = new_post_dict["visibility"]
    if "unlisted" in new_fields:
        post.unlisted = new_post_dict["unlisted"]
    if "contentType" in new_fields:
        post.content_type = new_post_dict["contentType"]

    post.save()

    return post