from django.urls import reverse_lazy
from auth_provider import user_resources

user_resources.register(resource_name='Posts', link_to_user_resource=reverse_lazy('posts:my-posts'))
