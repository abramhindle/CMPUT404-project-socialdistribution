# The purpose of this file is to contain "data transfer object" models.
# These are models designed to be used outside of a database context.
# These models do not have to be stored in a database, though they may 
# represent a model which is stored in the datbase. 
# 
# For example, a dto model might have additional fields that are used for 
# logic but do not have to be stored in the databse, or they may have fields
# that are deserialized versions of fields that are stored in a dabase.

import json
from re import match, search
from django.apps import apps

User = apps.get_model('core', 'User')

class Author:
    def __init__(self):
        self.type = "author"
        self.id = None
        self.url = None
        self.host = None
        self.displayName = None
        self.github = None
        self.profileImage = None

    @staticmethod
    def from_user(user: User, host):
        author = Author()
        author.id = host + "/service/author/" + str(user.id)
        author.url = host + "/service/author/" + str(user.id)
        author.host = host
        author.displayName = user.displayName if user.displayName else user.username
        author.github = user.github
        author.profileImage = user.profileImage
        return author

    @staticmethod
    def from_body(body: bytearray):
        return Author.from_json(body.decode('utf-8'))

    @staticmethod
    def from_json(json_str: str):
        data: dict = json.loads(json_str)
        author = Author()
        author.id = data["id"] if data.__contains__("id") else author.id
        author.url = data["url"] if data.__contains__("url") else author.url
        author.host = data["host"] if data.__contains__("host") else author.host
        author.displayName = data["displayName"] if data.__contains__("displayName") else author.displayName
        author.github = data["github"] if data.__contains__("github") else author.github
        author.profileImage = data["profileImage"] if data.__contains__("profileImage") else author.profileImage
        author.type = data["type"] if data.__contains__("type") else author.type

        return author

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, indent=4)

    @staticmethod
    def list_to_json(authors: list):
        return json.dumps(list(map(lambda x: x.__dict__, authors)), indent=4)

    def get_user_id(self):
        if (self.id):
            res = search('author/(.*)$', self.id)
            return res.group(1) if res else None
        else:
            return None

    '''
    Merges this author with the given user. Ignores this author's 
    id, url, and host because they can not be changed in the database.
    '''
    def merge_user(self, user: User):
        if (self.displayName != user.username):
            user.displayName = self.displayName

        user.github = self.github
        user.profileImage = self.profileImage
        return user