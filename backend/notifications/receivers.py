from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Notification
from comment.models import Comment
from comment.serializers import CommentSerializer
from authors.models import Author
import requests
from inbox.models import InboxItem
from concurrent.futures import ThreadPoolExecutor


