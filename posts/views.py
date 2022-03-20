from typing import Any, Dict
from django import forms
from django.db import transaction
from django.forms import ModelForm
from django.http import HttpResponseNotAllowed
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from posts.models import Post, Category, Comment, Like


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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            Like.objects.get(author=self.request.user, post=self.get_object())
            context['has_liked'] = True
        except Like.DoesNotExist:
            pass
        return context


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:my-posts')
    template_name = 'posts/delete_post.html'
    template_name_suffix = ''


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


class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 100
    template_name = 'posts/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date_published')


def like_post_view(request: HttpRequest, pk: int):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        Like.objects.get(author_id=request.user.id, post_id=pk)
    except Like.DoesNotExist:
        Like.objects.create(author_id=request.user.id, post_id=pk)
    return redirect(Post.objects.get(pk=pk).get_absolute_url())


def unlike_post_view(request: HttpRequest, pk: int):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        like = Like.objects.get(author_id=request.user.id, post_id=pk)
        like.delete()
    except Like.DoesNotExist:
        pass
    return redirect(Post.objects.get(pk=pk).get_absolute_url())
