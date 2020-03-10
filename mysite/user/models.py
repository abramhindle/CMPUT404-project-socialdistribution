from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .validators import UnicodeUsernameValidator

DEFAULTHOST = "http://127.0.0.1:3000/"

# Create your models here.
class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    email = models.EmailField(unique=True, editable=False)
    displayName = models.CharField(max_length=32, null=True, blank=True)
    host = models.URLField(default=DEFAULTHOST)
    github = models.URLField(null=True, blank=True)
    bio = models.TextField(max_length=2048, null=True, blank=True)
    is_approve = models.BooleanField(default=False)

    # Override
    username = models.CharField(
        _("username"),
        primary_key=True,
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator],
        error_messages={"unique": _("A user with that username already exists."),},
        editable=False,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
