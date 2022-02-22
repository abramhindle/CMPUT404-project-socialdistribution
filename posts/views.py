from django import forms
from django.db import transaction
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post, Category


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'categories']

    categories = forms.CharField(max_length=256)


class CreatePostView(LoginRequiredMixin, FormView):
    form_class = PostForm
    template_name = 'posts/post.html'

    def form_valid(self, form: PostForm) -> HttpResponse:
        form.instance.author = self.request.user

        with transaction.atomic():
            form.save()
            for category in form.cleaned_data['categories'].split(','):
                db_category = Category.objects.get_or_create(category=category)[0]
                form.instance.categories.add(db_category)
            form.save()
        return redirect('/')  # TODO: Update this when we have the post page
