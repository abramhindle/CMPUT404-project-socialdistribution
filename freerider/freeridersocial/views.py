from django.shortcuts import render

# Create your views here.

# http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
# http://service/author/posts (posts that are visible to the currently authenticated user)
# http://service/posts (all posts marked as public on the server)
# http://service/posts/{POST_ID} access to a single post with id = {POST_ID}

# http://service/posts/{post_id}/comments access to the comments in a post
# "query": "addComment"

# a reponse if friends or not
# GET http://service/author/<authorid>/friends/
# Ask if 2 authors are friends
# GET http://service/author/<authorid>/friends/<authorid2>
# ---------
# ask a service if anyone in the list is a friend
# POST to http://service/author/<authorid>/friends
# Here GREG tries to get a post from LARA that's marked as FOAF visibility
# the server will query greg's server to ensure that he is friends with 7de and 11c
# then it will get the users from its own server and see if they are friends of Lara
# Then it will go to at least 1 of these friend's servers and verify that they are friends of Greg
# once it is verified via the 3 hosts that Greg is a friend, then greg will get the data for lara's post
# POST to http://service/posts/{POST_ID} , sending the body
#{
#	"query":"getPost",
# then this returns with the generic GET http://service/posts/{POST_ID}
# ----------
# to make a friend request, POST to http://service/friendrequest

# Profile API calls
# GET http://service/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e
# Enables viewing of foreign author's profiles
