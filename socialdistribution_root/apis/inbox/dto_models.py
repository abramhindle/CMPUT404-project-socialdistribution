import json

class Inbox:
    def __init__(self):
        self.type = "inbox"
        self.author = None
        self.items = None

    @staticmethod
    def from_items(host, author_id, items):
        inbox = Inbox()
        inbox.author = host + "/author/" + str(author_id)
        inbox.items = list(map(lambda x: json.loads(x.item), items))
        return inbox

    def to_json(self, indent = 4):
        return json.dumps(self, default=lambda x: x.__dict__, indent=indent)

