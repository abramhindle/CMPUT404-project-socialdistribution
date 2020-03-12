from django.core.management.base import BaseCommand, CommandError
import csv
from sd.models import Post, Author, Comment, FriendRequest, Follow, Friend


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
                            content=row[1],
                            visibility=row[2]
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
                            comment=row[0],
                            post = self.posts[p]
                        )
                    comments.append(c)

                    a = (a + 1) % 5
                    p = (p + 1) % 25

        return comments

    def send_friend_request(self):
        # one_auth wants to befriend two_auth
        # three_auth wants to befriend four_auth
        FriendRequest.objects.get_or_create(
            to_author = self.authors[1],
            from_author = self.authors[0]
        )

        FriendRequest.objects.get_or_create(
            to_author = self.authors[3],
            from_author = self.authors[2]
        )

    def follow(self):
        # one_auth follows three_auth
        # two_auth follows four_auth
        Follow.objects.get_or_create(
            follower = self.authors[0],
            following = self.authors[2]
        )

        Follow.objects.get_or_create(
            follower = self.authors[1],
            following = self.authors[3]
        )

    def friend(self):
        # one_auth is friends with five_auth
        # two_auth is friends with five_auth
        # four_auth is friends with five_auth
        # five_auth is popular
        pass
