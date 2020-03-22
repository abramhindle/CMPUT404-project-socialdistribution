from django import forms

from .models import (Comment,
                     Post)
from PIL import Image
from datetime import datetime

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
            # 'visibileTo',
            'published',
            'content_type',
            'content',
            'image_file',
            'unlisted',
        ]
        widgets = {
            'title' :forms.Textarea(attrs={'cols':89,'rows': 1, 'placeholder': 'Title','required':'True'}),
            'content' :forms.Textarea(attrs={'cols':89,'rows': 4, 'placeholder': 'Content', 'required':'True'}),
            # 'visibileTo':forms.Textarea(attrs={'cols':89,'rows': 4, 'placeholder': 'Visibile To'}),
            'published': forms.SelectDateWidget()
            # 'published' : forms.DateField(widget=forms.SelectDateWidget(), label='Joining Date', initial=datetime.now())
            # 'published' : forms.SelectDateWidget(initial=datetime.now())
            # 'published' : forms.DateField(widget=forms.DateInput(attrs={'class':'timepicker'}))
            # 'published' : forms.DateTimeField()
            
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
