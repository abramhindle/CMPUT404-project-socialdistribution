class Post(object):
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