from django import forms
from django.db import transaction
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post, Category, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'categories']

    categories = forms.CharField(max_length=256)


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def form_valid(self, form: PostForm) -> HttpResponse:
        form.instance.author = self.request.user

        with transaction.atomic():
            form.save()
            for category in form.cleaned_data['categories'].split(','):
                db_category = Category.objects.get_or_create(category=category.strip())[0]
                form.instance.categories.add(db_category)
            form.save()
        return redirect(form.instance.get_absolute_url())


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/edit_post.html'

    def get_initial(self):
        initial = super().get_initial()
        # Inject categories to text field
        categories = [str(category.category) for category in Post.objects.get(pk=self.kwargs['pk']).categories.all()]
        initial['categories'] = ', '.join(categories)
        return initial

    def form_valid(self, form: PostForm) -> HttpResponse:
        with transaction.atomic():
            form.save()
            for category in form.cleaned_data['categories'].split(','):
                db_category = Category.objects.get_or_create(category=category)[0]
                form.instance.categories.add(db_category)
            form.save()
        return redirect(form.instance.get_absolute_url())


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['author', 'post']


class CreateCommentView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = 'comments/create_comment.html'

    def form_valid(self, form: PostForm) -> HttpResponse:
        post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        form.save()
        return redirect(post.get_absolute_url())
