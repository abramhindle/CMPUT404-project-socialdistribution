from profiles.models import Author
from posts.models import Post, Comment


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
        "published" : post.published,
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
        "published" : comment.published,
        "id" : comment.id    
    }