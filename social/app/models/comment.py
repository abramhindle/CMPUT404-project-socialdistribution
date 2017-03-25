from django.db import models

from social.app.models.author import Author
from social.app.models.post import Post


# Based on code by Django Girls, url:
# https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/homework_create_more_models/
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="author of the comment",
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}: {}'.format(self.author, self.post, self.text)
