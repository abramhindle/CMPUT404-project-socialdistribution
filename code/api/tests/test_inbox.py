# python manage.py test api

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
import json

from socialDistribution.models import Author, Inbox, Post

# Documentation and code samples taken from the following references:
# Django Software Foundation, https://docs.djangoproject.com/en/3.2/intro/tutorial05/
# Django Software Foundation, https://docs.djangoproject.com/en/3.2/topics/testing/overview/
# Python Software Foundation, https://docs.python.org/3/library/unittest.html


def create_author(id, username, displayName, githubUrl):
    user = mixer.blend(User, username=username)
    author = Author.objects.create(
        id=id, username=username, displayName=displayName, githubUrl=githubUrl, user=user)
    inbox = Inbox.objects.create(author=author)
    return author, inbox


class InboxViewTests(TestCase):

    def test_post_local_follow(self):
        author1, inbox1 = create_author(
            1,
            "user1",
            "Greg Johnson",
            "http://github.com/gjohnson"
        )
        author2, inbox2 = create_author(
            2,
            "user2",
            "Lara Croft",
            "http://github.com/laracroft"
        )

        body = {
            "type": "follow",
            "summary": "Greg wants to follow Lara",
            "actor": {
                "type": "author",
                "id": "http://127.0.0.1:8000/api/author/1",
                "url": "http://127.0.0.1:8000/api/author/1",
                "host": "http://127.0.0.1:8000/api/",
                "displayName": "Greg Johnson",
                "github": "http://github.com/gjohnson",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "object": {
                "type": "author",
                "id": "http://127.0.0.1:8000/api/author/2",
                "host": "http://127.0.0.1:8000/api/",
                "displayName": "Lara Croft",
                "url": "http://127.0.0.1:8000/api/author/2",
                "github": "http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            }
        }

        response = self.client.post(
            reverse("api:inbox", kwargs={"author_id": 2}),
            content_type="application/json",
            data=body
        )

        self.assertEqual(response.status_code, 200)

        query_set = author2.inbox.follow_requests.all()
        self.assertEqual(query_set.count(), 1)
        self.assertEqual(query_set[0], author1)

    def test_post_local_post(self):
        # NOTE: This test is very basic. More work needed on this endpoint.
        
        author1, inbox1 = create_author(
            1,
            "user1",
            "Greg Johnson",
            "http://github.com/gjohnson"
        )
        author2, inbox2 = create_author(
            2,
            "user2",
            "Lara Croft",
            "http://github.com/laracroft"
        )

        # Create a post from author1
        dummy_post = mixer.blend(Post, id=1, author=author1)

        body = {
            "type": "post",
            "title": "A Friendly post title about a post about web dev",
            "id": "http://127.0.0.1:8000/api/author/1/posts/1",  # this is the only line being parsed right now!
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "This post discusses stuff -- brief",
            "contentType": "text/plain",
            "content": "Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
            "author": {
                "type": "author",
                "id": "http://127.0.0.1:8000/author/4",
                "host": "http://127.0.0.1:8000/",
                "displayName": "Lara Croft",
                "url": "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "github": "http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "categories": ["web", "tutorial"],
            "comments": "http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
            "published": "2015-03-09T13:07:04+00:00",
            "visibility": "FRIENDS",
            "unlisted": False
        }

        # Send the post to author 2
        response = self.client.post(
            reverse("api:inbox", kwargs={"author_id": 2}),
            content_type="application/json",
            data=body
        )

        self.assertEqual(response.status_code, 200)

        # Check the received posts of author2
        query_set = author2.inbox.posts.all()
        self.assertEqual(query_set.count(), 1)
        self.assertEqual(query_set[0], dummy_post)

