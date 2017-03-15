from __future__ import unicode_literals

import CommonMark
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver

from dashboard.models import Author


class Post(models.Model):
    post_story = models.TextField()
    post_story_html = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="author of the post",
    )
    image = models.FileField(null=True, blank=True)
    use_markdown = models.BooleanField(default=False)
    # Code idea from Django Docs,
    # url: https://docs.djangoproject.com/en/dev/ref/models/fields/#choices
    visibilityOptions = [("PUBLIC", "Public"), ("FOAF", "FOAF"),
                         ("FRIENDS", "Friends"), ("PRIVATE", "Private"), ("SERVERONLY", "This Server Only")]
    visibility = models.CharField(
        max_length=10,
        choices=visibilityOptions,
        default="PUBLIC",
    )

    # This will be a choice from author's friends
    # defaults to []
    # attribute only renders in /post/add/ if visibility is set to "PRIVATE"
    visibleTo = models.ManyToManyField(Author, related_name='visible_posts')

    def get_absolute_url(self):
        '''
        Add new post to database
        '''
        return reverse('posts:detail', kwargs={'pk': self.pk})

    # Print the string representation of Post
    def __str__(self):
        return self.post_story


# Pre-save code based on idea by
# Bernhard Vallant (http://stackoverflow.com/users/183910/bernhard-vallant)
# from http://stackoverflow.com/a/6462188/2557554 and licensed under
# CC-BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0/deed.en)
@receiver(pre_save, sender=Post)
def update_post_story_html(sender, instance, *args, **kwargs):
    post_story_html = instance.post_story

    if instance.use_markdown:
        parser = CommonMark.Parser()
        renderer = CommonMark.HtmlRenderer(options={'safe': True})
        post_story_html = renderer.render(parser.parse(post_story_html))

    instance.post_story_html = post_story_html


# Based on code by Django Girls, url: https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/homework_create_more_models/
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
