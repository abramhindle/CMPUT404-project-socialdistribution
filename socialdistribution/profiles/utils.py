from profiles.models import AuthorFriend


def getFriendsOfAuthor(author):
    friends = []
    # Find all people that the author follows
    author_friends = AuthorFriend.objects.filter(author=author)
    # Find all people that follow author
    friends_author = AuthorFriend.objects.filter(friends=author)

    # Friend if author follows person and person follows author back
    for object in author_friends:
        # Check if the people that the author follows also follows them back
        if friends_author.filter(author=object.friend):
            friends.append(object)
    return friends


def getFriendRequestsToAuthor(author):
    friend_requests_to_author = []
    # Find all people that the author follows
    author_friends = AuthorFriend.objects.filter(author=author)
    # Find all people that follow author
    friends_author = AuthorFriend.objects.filter(friends=author)

    # Friend request if person follows author but author does not follow back
    for object in friends_author:
        # If author does not follow them back then it is a friend request
        if not author_friends.filter(friend=object.author):
            friend_requests_to_author.append(object)
    return friend_requests_to_author


def getFriendRequestsFromAuthor(author):
    friend_requests_from_author = []
    # Find all people that the author follows
    author_friends = AuthorFriend.objects.filter(author=author)
    # Find all people that follow author
    friends_author = AuthorFriend.objects.filter(friends=author)

    # Friend request sent if author follows person but person does not
    # follow back
    for object in author_friends:
        # If person does not follow author then it is a friend request
        if not friends_author.filter(friend=object.author):
            friend_requests_from_author.append(object)
    return friend_requests_from_author
