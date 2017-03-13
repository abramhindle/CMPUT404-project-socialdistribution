from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
from dashboard.forms import UserProfileFormUpdate, UserFormUpdate
from dashboard.models import Author
from post.models import Post
from django.db.models import Q


def index(request):
    # Note: Slight modification to allow for latest posts to be displayed on landing page
    if request.user.is_authenticated():
        # Return posts only by current user
        user = request.user
        context = dict()
        context['user_posts'] = Post.objects.filter(author__id=user.profile.id).order_by('-pub_date')
        return render(request, 'dashboard/index.html', context)
    else:
        # Return all posts on present on the site
        context = dict()
        context['all_posts'] = Post.objects.all().order_by('-pub_date')
        return render(request, 'dashboard/landing.html', context)


def indexHome(request):
    # Note: Slight modification to allow for latest posts to be displayed on landing page
    if request.user.is_authenticated():
        user = request.user
        author = Author.objects.get(user=request.user.id)
        context = dict()
        context1 = dict()
        context2 = dict()

        # Return posts that are NOT by current user (=author) and:

        # case 1: post.visibility=public and following               --> can view
        # case 1': post.visibility=public  and not following          --> can't view
        # case 2': post.visibility=friends and not friends            --> can't view
        context1['all_posts'] = Post.objects\
            .filter(~Q(author__id=user.profile.id))\
            .filter(author__id__in=author.followed_authors.all()) \
            .filter(visibility="PUBLIC").order_by('-pub_date')

        # case 2: post.visibility=friends and friends                 --> can view
        context2['all_posts'] = Post.objects \
            .filter(~Q(author__id=user.profile.id)) \
            .filter(author__id__in=author.friends.all()) \
            .filter(Q(visibility="FRIENDS")|Q(visibility="PUBLIC")).order_by('-pub_date')

        context["all_posts"] = context1["all_posts"] | context2["all_posts"]

        # TODO: need to be able to filter posts by current user's relationship to post author
        # case 3: post.visibility=foaf and friend/foaf                --> can view
        # case 3': post.visibility=foaf and not either friend/foaf    --> can view
        # case 4: post.visibility=private                             --> can't see

        return render(request, 'dashboard/indexhome.html', context)

    else:
        # Return all posts on present on the site
        context = dict()
        context['all_posts'] = Post.objects.all().order_by('-pub_date')
        return render(request, 'dashboard/landing.html', context)


def profile(request):
    user = request.user
    user_profile = user.userprofile


@login_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_form = UserFormUpdate(instance=user)

    profile_inline_formset = inlineformset_factory(
        User, Author,
        fields=('displayName', 'github', 'bio'))
    formset = profile_inline_formset(instance=user)
    formset.can_delete = False

    if request.user.is_authenticated() and request.user.id == user.id:

        if request.method == "POST":
            user_form = UserFormUpdate(request.POST, request.FILES, instance=user)
            formset = profile_inline_formset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)

                formset = profile_inline_formset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    messages.success(request, 'Your profile has been updated successfully!', extra_tags='alert-success')
                    return HttpResponseRedirect('/accounts/' + str(user.id))
                else:
                    messages.error(request, 'Oops! There was a problem updating your profile!',
                                   extra_tags='alert-danger')

        return render(request, "account/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'dashboard/authors_list.html'
    context_object_name = 'all_authors'

    def get_queryset(self):
        return Author.objects.all().order_by('-displayName')


class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        logged_in_author = self.request.user.profile
        detail_author = context["object"]

        context['show_follow_button'] = \
            logged_in_author != detail_author \
            and not logged_in_author.follows(detail_author)

        context['show_unfollow_button'] = logged_in_author.follows(detail_author)
        context['show_friend_request_button'] = logged_in_author.can_send_a_friend_request_to(detail_author)
        context['outgoing_friend_request_for'] = logged_in_author.has_outgoing_friend_request_for(detail_author)
        context['incoming_friend_request_from'] = logged_in_author.has_incoming_friend_request_from(detail_author)
        context['is_friends'] = logged_in_author.friends_with(detail_author)

        return context


class FriendRequestsListView(generic.ListView):
    context_object_name = "all_friend_requests"
    template_name = "dashboard/friend_requests_list.html"

    def get_queryset(self):
        return self.request.user.profile.incoming_friend_requests.all()
