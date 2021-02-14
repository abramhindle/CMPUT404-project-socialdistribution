from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
import uuid


# class AuthorManager(BaseUserManager):
#     def create_uesr(self, email, password=None, **extra):
#         user = self.model(
#             email=self.normalize_email(email),
#             **extra
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password, **extra):
#         user = self.create_user(
#             email,
#             password=password,
#             **extra
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

class Author(AbstractUser):
    # model for author
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    authorID = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    github = models.URLField(max_length=200, blank=True)

    USERNAME_FIELD = 'email' # use email to login
    REQUIRED_FIELDS = ['username']

    #objects = AuthorManager()

    def __str__(self):
        return self.email

    def has_perms(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Post(models.Model):
    title = models.CharField(max_length=100)
    postID = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    description = models.TextField()
    contentType = models.CharField(max_length=20)
    content = models.TextField()
    # author field
    # categories
    count = models.IntegerField()
    size = models.IntegerField()
    comments = models.CharField(max_length=200)
    # comments dict
    published = models.DateField(auto_now_add=True)
    visibility = models.CharField(max_length=10, default="PUBLIC")
    unlisted = models.BooleanField(default=False)
