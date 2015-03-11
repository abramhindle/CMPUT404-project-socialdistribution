from django.db import models


class Node(models.Model):
    """A Node represents a server that Social Distribution communicate's with.

    Social Distribution itself is a Node and will make API calls to other Nodes
    in order to send friend requests to Authors on that server. In return,
    Social Distribution will also allow other Nodes to make API requests to us.
    """
    name = models.CharField(max_length=64, blank=True)
    host = models.CharField(max_length=124, blank=True)

    def __unicode__(self):
        return '%s: %s' % (name, host)

class PostInfo(object):
        def __init__(self):
            self.title= ""
            self.source= ""
            self.origin= "" 
            self.description = ""
            self.content_type= ""
            self.content=""
            self.author={"id":"",
                        "host":"",
                        "displayname":"",
                        "url":""
                        },
            self.categories=[]
            self.comments=[
                    {
                        "author":{
                            "id":"",
                            "host":"",
                            "displayname":""
                        },
                        "comment":"",
                        "pubDate":"",
                        "guid":""
                    }
            ]
            self.pubDate=""
            self.guid=""
            self.visibility=""
