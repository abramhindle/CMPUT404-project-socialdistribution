from profiles.models import Author, AuthorFriend


def getFriends(author):
    friends = []
    author_friends = Author.objects.filter(author=author)
    friends_author = Author.objects.filter(friends=author)

    for friend in author_friends:
        if friends_author.filter(friend=author):
            friends.append(friend)


    return friends

def getFriendRequests(author):
    pass
