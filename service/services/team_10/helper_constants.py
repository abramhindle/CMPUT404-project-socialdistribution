from django.conf import settings

AUTH = {'Authorization': 'Token ' + settings.REMOTE_USERS[3][2]}
HOST = settings.REMOTE_USERS[3][1]