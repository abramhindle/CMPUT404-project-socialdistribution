from apps.core.models import Author, User

USERNAME = "admin"
EMAIL = "admin@ualberta.ca"
PASSWORD = "admin"

class AuthHelper:
    def __init__(self):
        self.author = None
        
    def setup(self):
        user = User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        self.author = Author.objects.get(userId=user.id)

    def authorize_client(self, client):
        client.login(username=USERNAME, password=PASSWORD)

    def get_author(self):
        return self.author