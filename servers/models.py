from typing import Dict
from django.db import models
from requests.auth import HTTPBasicAuth
import requests

STR_MAX_LENGTH = 512


class Server(models.Model):
    service_address = models.CharField(max_length=STR_MAX_LENGTH)
    username = models.CharField(max_length=STR_MAX_LENGTH)
    password = models.CharField(max_length=STR_MAX_LENGTH)

    def get(self, endpoint: str, params: Dict[str, str] = []) -> requests.Response:
        full_endpoint = self.service_address + endpoint
        return requests.get(full_endpoint, params, auth=HTTPBasicAuth(self.username, self.password))
