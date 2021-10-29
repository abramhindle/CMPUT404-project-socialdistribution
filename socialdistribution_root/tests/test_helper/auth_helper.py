from apps.core.models import User

USERNAME = "admin"
EMAIL = "admin@ualberta.ca"
PASSWORD = "admin"

class AuthHelper:
    def __init__(self):
        self.user = None
        
    def setup(self):
        self.user = User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)

    def authorize_client(self, client):
        client.login(username=USERNAME, password=PASSWORD)

    def get_super_user(self):
        return self.user