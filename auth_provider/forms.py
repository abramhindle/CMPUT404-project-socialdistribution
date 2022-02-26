from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'github_url', 'profile_image_url')

    def save(self, commit=True):
        user = super().save(commit)
        # Require server to set active manually by default
        user.is_active = False
        if commit:
            user.save()
        return user
