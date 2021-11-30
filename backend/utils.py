from .models import Author, FriendRequest, Post, Comment, Like, Inbox


def get_author(author_id: str) -> Author:
    try:
        author = Author.objects.get(id=author_id)
    except:
        return None
    return author

# Helper function on getting the follower from an author using the follower_id
def get_follower(author: Author, follower_id: str) -> Author:
    try:
        follower = author.followers.get(id=follower_id)
    except:
        return None
    return follower

# Helper function on getting the friend from an author using the friend_id
def get_friend(author: Author, friend_id: str) -> Author:
    try:
        author.followers.get(id=friend_id)
        friend = get_author(friend_id)
        friend.followers.get(id=author.id)
    except:
        return None
    return friend

# Helper function on getting the post from an author object
def get_post(author: Author, post_id: str) -> Post:
    try:
        post = author.posted.get(id=post_id)
    except:
        return None
    return post

# Helper function on getting the comment from a post object
def get_comment(post: Post, comment_id) -> Comment:
    try:
        comment = post.comments.get(id=comment_id)
    except:
        return None
    return comment

# Helper function on getting the friend request from an author using the friend_id
def get_friend_request(sender: Author, recipient: Author) -> FriendRequest:
    try:
        friend_request = FriendRequest.objects.get(object = recipient, actor = sender)
        return friend_request
    except:
        return None
    