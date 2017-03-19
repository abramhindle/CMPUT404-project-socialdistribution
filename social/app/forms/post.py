from django import forms

from social.app.models.post import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['post_story', 'use_markdown', 'visibility', 'image']
