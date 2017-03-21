from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.db.models import Q

from social.app.forms.user_profile import UserFormUpdate
from social.app.models.author import Author
from social.app.models.post import Post


def view_posts_by_author(request, pk):
    current_user = request.user
    author = Author.objects.get(id=pk)
    author_guid = str(pk)
    current_author = Author.objects.get(user=request.user.id)
    current_author_guid = str(current_author.id)

    # If current user is authenticated and the guid in the url is the same as the current user's guid
    # then show them their own posts
    if (current_user.is_authenticated() and current_author_guid == author_guid):
        context = dict()
        # Return all posts by current user
        context['user_posts'] = Post.objects.filter(author__id=current_user.profile.id).order_by('-pub_date')
        context['show_add_post_button'] = "true"
        return render(request, 'app/index.html', context)

    # If the current user is authenticated only show them the posts that are visible to them
    elif current_user.is_authenticated():
        context = dict()
        context1 = dict()
        context2 = dict()

        # case 1:  posts.visibility=public and following               --> can view
        # case 1': posts.visibility=public  and not following          --> can view
        # case 2': posts.visibility=friends and not friends            --> can't view
        context1['user_posts'] = Post.objects \
            .filter(author__id=author.id) \
            .filter(visibility="PUBLIC").order_by('-pub_date')

        # case 2: posts.visibility=friends and friends                 --> can view
        context2['user_posts'] = Post.objects \
            .filter(author__id=author.id) \
            .filter(author__id__in=current_author.friends.all()) \
            .filter(visibility="FRIENDS").order_by('-pub_date')

        context["user_posts"] = context1["user_posts"] | context2["user_posts"]
        context['show_add_post_button'] = "false"
        return render(request, 'app/index.html', context)

    # If not authenticated
    else:
        context = dict()
        context['user_posts'] = Post.objects \
            .filter(author__id=author.id) \
            .filter(visibility="PUBLIC").order_by('-pub_date')
        context['show_add_post_button'] = "false"
        return render(request, 'app/index.html', context)


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
    template_name = 'app/authors_list.html'
    context_object_name = 'all_authors'

    def get_queryset(self):
        return Author.objects.all().order_by('-displayName')


class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        logged_in_author = self.request.user.profile
        detail_author = context["object"]

        context['show_follow_button'] = logged_in_author.can_follow(detail_author)
        context['show_unfollow_button'] = logged_in_author.follows(detail_author)
        context['show_friend_request_button'] = logged_in_author.can_send_a_friend_request_to(detail_author)
        context['outgoing_friend_request_for'] = logged_in_author.has_outgoing_friend_request_for(detail_author)
        context['incoming_friend_request_from'] = logged_in_author.has_incoming_friend_request_from(detail_author)
        context['is_friends'] = logged_in_author.friends_with(detail_author)

        return context
