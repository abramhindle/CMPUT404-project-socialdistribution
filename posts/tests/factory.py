from posts.models import User, Post, Comment, Category

class GeneralFunctions:

    def generate_random_word(self, n):
        word = ''
        for i in range(n):
            word += random.choice(string.ascii_letters)
        return word

    def create_user(self, username="test1", email="test@test.com", password="password1", approved=False):
        data = {'username': username, 'first_name': 'testFirstName',
                'last_name': 'testLastName', 'email': email, 'approved':approved}
        user = User.objects.create(**data)
        user.set_password(password)
        # user.approved = True
        user.save()
        return user

    def create_post(self, title, user):
        data = {
            "title": title, "description": "this is a description",
            "content": "This is some content", "author": user
        }
        post = Post.objects.create(**data)
        post.save()
        return post

    def create_comment(self, post, author, comment="default comment"):
        data = {
            "parent_post": post, "author": author, "comment": comment
        }
        comment = Comment.objects.create(**data)
        comment.save()
        return comment

def create_users(usernames):
    for username in usernames:
        email = username + '@' + 'email.com'
        FACTORY.create_user(username=username, email=email)

def create_posts(post_titles):
    users = User.objects.all()
    smaller = min(len(users), len(post_titles))
    for i in range(smaller):
        FACTORY.create_post(post_titles[i], users[i])

def create_comments(comments):
    users = User.objects.all()
    posts = Post.objects.all()

    smaller = min(len(users), len(posts))
    """ create 2 comments max """
    for i in range(min(smaller, 2)):
        FACTORY.create_comment(posts[i], users[i], comment=comments[i])

def delete_all():
    Post.objects.all().delete()
    User.objects.all().delete()
    Comment.objects.all().delete()
    Category.objects.all().delete()

FACTORY = GeneralFunctions()
def generate():

    usernames = ["alpha", "bravo", "charlie", "delta"]
    post_titles = ["title1", "title2", "title3", "title4"]
    comments = ["this is comment 1", "this is comment 2"]

    create_users(usernames)
    create_posts(post_titles)
    create_comments(comments)

def refresh():
    delete_all()
    generate()



# from posts.tests import factory
