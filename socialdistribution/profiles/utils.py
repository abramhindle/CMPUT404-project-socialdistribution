from profiles.models import AuthorFriend


def getFriends(author):
    friends = []
    # Find all people that the author follows
    author_friends = AuthorFriend.objects.filter(author=author)
    # Find all people that follow author
    friends_author = AuthorFriend.objects.filter(friends=author)

    # Friend if both follow each other
    for object in author_friends:
        # Check if the people that the author follows also follows them back
        if friends_author.filter(author=object.friend):
            friends.append(object)
    return friends


def getFriendRequests(author):
    friend_requests = []
    # Find all people that the author follows
    author_friends = AuthorFriend.objects.filter(author=author)
    # Find all people that follow author
    friends_author = AuthorFriend.objects.filter(friends=author)

    # Friend request if author does not follow back
    for object in friends_author:
        # If author does not follow them back then it is a friend request
        if not author_friends.filter(friend=object.author):
            friend_requests.append(object)
    return friend_requests


def getSentRequests(author):
    friend_requests_sent = []
    # Find all people that the author follows
    author_friends = AuthorFriend.objects.filter(author=author)
    # Find all people that follow author
    friends_author = AuthorFriend.objects.filter(friends=author)

    # Friend if both follow each other
    for object in author_friends:
        # If person does not follow author then it is a friend request
        if not friends_author.filter(friend=object.author):
            friend_requests_sent.append(object)
    return friend_requests_sent
