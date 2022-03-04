from typing import Any, Dict, Optional
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, logout
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from .user_resources import user_resources
from .forms import SignUpForm, EditProfileForm
from .user_action_generators import UserActionGenerator, user_action_generators


class SignUpView(CreateView):
    template_name = 'auth/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('auth_provider:login')


class MyProfileView(DetailView):
    model = get_user_model()
    template_name = 'profile/my_profile.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_resources'] = [{'name': user_resource[0], 'link': user_resource[1]}
                                     for user_resource in user_resources]
        return context


class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'profile/user_profile.html'

    def get_context_object_name(self, obj: Any) -> Optional[str]:
        return 'object'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        def get_action(user_action_generator: UserActionGenerator):
            user_action = user_action_generator(self.request.user, self.get_object())
            if user_action is None:
                return None
            return {
                'name': user_action[0],
                'link': user_action[1],
            }

        # TODO: Clean this up with a lambda
        actions = [get_action(user_action_generator)
                   for user_action_generator in user_action_generators]
        context['user_actions'] = []
        for action in actions:
            if action is not None:
                context['user_actions'].append(action)

        return context


class EditProfileView(UpdateView):
    form_class = EditProfileForm
    model = get_user_model()
    template_name = 'profile/edit_profile.html'

    def get_object(self):
        return self.request.user


def logout_view(request):
    logout(request)
    return redirect('/')
