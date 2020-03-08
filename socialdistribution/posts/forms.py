from django import forms

from .models import (Comment,
                     Post)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'description',
            'author',
            'categories',
            'visibility',
            'visibileTo',
            'published',
            'image_file',
        ]
        widgets = {
            'title' :forms.Textarea(attrs={'cols':89,'rows': 1, 'placeholder': 'Title','required':'True'}),
            'description' :forms.Textarea(attrs={'cols':89,'rows': 4, 'placeholder': 'Description', 'required':'True'}),
            'visibileTo':forms.Textarea(attrs={'cols':89,'rows': 4, 'placeholder': 'visibileTo'}),
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
