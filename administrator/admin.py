from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            self.Meta.model.objects.get(username__iexact=username)
        except self.Meta.model.DoesNotExist:
            return username

        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

def approveUsers(modeladmin, request, queryset):
	queryset.update(is_active=True)

def UnApproveUsers(modeladmin, request, queryset):
	queryset.update(is_active=False)
       
class Admin(UserAdmin):
    list_filter = []
    search_fields = []
    exclude = []
    actions = [approveUsers,UnApproveUsers]

    ordering = ('date_joined','username',)
    list_display = ('username', 'email','date_joined', 'is_active','is_staff')
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )

approveUsers.short_description = "Approve user"
UnApproveUsers.short_description = "UnApprove user"

admin.site.unregister(User)
admin.site.register(User, Admin)
