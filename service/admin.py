from django import forms
from django.contrib import admin
from service.models import author, post, comment, like, inbox, follow
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# Register your models here.
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = author.Author
        fields = ('username', 'password', 'displayName', 'profileImage', 'github')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = author.Author
        fields = ('username', 'password', 'is_active', 'is_local', 'displayName', 'profileImage', 'github')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('_id', 'is_active', 'displayName', 'profileImage', 'github')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('displayName', 'profileImage', 'github')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_local')}),
    )
    # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # # overrides get_fieldsets to use this attribute when creating a user.
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('is_active', 'displayName', 'profileImage', 'github'),
    #     }),
    # )
    # search_fields = ('email',)
    # ordering = ('email',)
    # filter_horizontal = ()


admin.site.register(author.Author, UserAdmin)
#admin.site.register(follow.Followers)
admin.site.register(post.Post) #we don't need this here, but leaving as comment just in case
#admin.site.register(post.Category)
admin.site.register(like.Like)
admin.site.register(comment.Comment)
# admin.site.register(follow.Followers)
#admin.site.register(inbox.Inbox)