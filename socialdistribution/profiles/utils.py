from profiles.models import AuthorFriend


def getAuthorFriendRelationships(author):
    all_author_friend_entries = AuthorFriend.objects.all()
    # Find all people that the author follows
    author_friends = all_author_friend_entries.filter(author=author)
    # Find all people that follow author
    friends_author = all_author_friend_entries.filter(friend=author)

    return author_friends, friends_author


def getFriendsOfAuthor(author):
    friends = []
    author_friends, friends_author = getAuthorFriendRelationships(author)

    # Friend if author follows person and person follows author back
    for object in author_friends:
        # Check if the people that the author follows also follows them back
        if friends_author.filter(author=object.friend):
            friends.append(object)
    return friends


def getFriendRequestsToAuthor(author):
    friend_requests_to_author = []
    author_friends, friends_author = getAuthorFriendRelationships(author)

    # Friend request if person follows author but author does not follow back
    for object in friends_author:
        # If author does not follow them back then it is a friend request
        if not author_friends.filter(friend=object.author):
            friend_requests_to_author.append(object)
    return friend_requests_to_author


def getFriendRequestsFromAuthor(author):
    friend_requests_from_author = []
    author_friends, friends_author = getAuthorFriendRelationships(author)

    # Friend request sent if author follows person but person does not
    # follow back
    for object in author_friends:
        # If person does not follow author then it is a friend request
        if not friends_author.filter(friend=object.author):
            friend_requests_from_author.append(object)
    return friend_requests_from_author
