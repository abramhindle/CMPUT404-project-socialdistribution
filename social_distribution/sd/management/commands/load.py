from django.core.management.base import BaseCommand, CommandError
import csv
from sd.models import Post, Author, Comment, FriendRequest, Follow, FriendList


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.authors = self.create_authors()
        self.posts = self.create_posts()
        self.comments = self.create_comments()
       

    def create_authors(self):
        authors = []
        with open("test_data/authors.csv") as f:
                reader = csv.reader(f, delimiter=";")
                for row in reader:
                    a, _ = Author.objects.get_or_create(
                            first_name=row[0],
                            last_name=row[1],
                            bio=row[2],
                            username=row[3]
                        )
                    authors.append(a)

        return authors

    def create_posts(self):
        posts = []
        with open("test_data/posts.csv") as f:
                reader = csv.reader(f, delimiter=";")
                a = 0
                for row in reader:
                    p, _ = Post.objects.get_or_create(
                            author = self.authors[a],
                            title=row[0],
                            body=row[1],
                            status=row[2]
                        )
                    posts.append(p)

                    a = (a + 1) % 5

        return posts

    def create_comments(self):
        comments = []
        with open("test_data/comments.csv") as f:
                reader = csv.reader(f, delimiter=";")
                a = 0
                p = 0
                for row in reader:
                    c, _ = Comment.objects.get_or_create(
                            author = self.authors[a],
                            body=row[0],
                            post = self.posts[p]
                        )
                    comments.append(c)

                    a = (a + 1) % 5
                    p = (p + 1) % 25

        return comments