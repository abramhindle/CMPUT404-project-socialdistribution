from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from dashboard.models import Author


class Post(models.Model):
    post_story = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="author of the post",
    )
    image = models.FileField(null=True, blank=True)

    def get_absolute_url(self):
        '''
        Add new post to database
        '''
        return reverse('post:detail', kwargs={'pk': self.pk})

    # Print the string representation of Post
    def __str__(self):
        return self.post_story


# Based on code by Django Girls, url: https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/homework_create_more_models/
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    author = models.CharField(max_length=80)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.post)

