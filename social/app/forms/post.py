from django import forms

from social.app.models.post import Post


class TextPostForm(forms.ModelForm):
    content_type = forms.ChoiceField(choices=Post.TEXT_CONTENT_TYPES)
    categories = forms.CharField(
        label="Categories",
        required=False,
        help_text="Space-delimited",
    )

    class Meta:
        model = Post
        fields = ["title", "description", "content_type", "content", "visibility", "visible_to",
                  "unlisted"]
