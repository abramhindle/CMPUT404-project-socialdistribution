from django import forms

from .models import (Comment,
                     Post)
from PIL import Image
from datetime import datetime
from bootstrap_datepicker_plus import DateTimePickerInput

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
            'published',
            'content_type',
            'content',
            'image_file',
            'unlisted',
        ]
        widgets = {
            'title' :forms.Textarea(attrs={'cols':89,'rows': 1, 'placeholder': 'Title','required':'True'}),
            'content' :forms.Textarea(attrs={'cols':89,'rows': 4, 'placeholder': 'Content', 'required':'True'}),
            'published':  DateTimePickerInput()
    
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
