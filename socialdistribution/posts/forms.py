from django import forms

from .models import (Comment,
                     Post)
from PIL import Image

class PostForm(forms.ModelForm):
    image_file = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = [
            'title',
            'description',
            'author',
            'categories',
            'visibility',
            'visibleTo',
            'published',
            'contentType',
            'content',
            'image_file',
            'unlisted',
        ]
        widgets = {
            'title' :forms.Textarea(attrs={'cols':89,'rows': 1, 'placeholder': 'Title','required':'True'}),
            'content' :forms.Textarea(attrs={'cols':89,'rows': 4, 'placeholder': 'Content', 'required':'True'}),
            'visibleTo':forms.Textarea(attrs={'cols':89,'rows': 4, 'placeholder': 'Visible To'}),
            'published': forms.SelectDateWidget()

        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            #'author',
            'comment',
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'cols':80,'rows': 5, 'placeholder': 'Leave a comment...'})
        }
