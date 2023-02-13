from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Post


class IndexView(generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'latest_posts'

    def get_queryset(self):
        """Return the last five published questions."""
        try:
          return Post.objects.order_by('-pub_date')[:5]
        except: 
          pass


class DetailView(generic.DetailView):
    model = Post
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Post
    template_name = 'polls/results.html'

def post(request):
    try:
        post = get_object_or_404(Post)
    except (KeyError, Post.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'templates/posts/detail.html', {
            'error_message': "You didn't make a post.",
        })
    else:
        post.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(post.id,)))