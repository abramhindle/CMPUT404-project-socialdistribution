from django import forms

from social.app.models.comment import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
