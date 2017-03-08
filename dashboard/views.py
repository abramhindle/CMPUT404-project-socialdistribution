from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

# Create your views here.
from dashboard.forms import UserProfileFormUpdate, UserFormUpdate
from dashboard.models import UserProfile


def index(request):
    if not request.user.is_authenticated():
        return render_to_response('dashboard/landing.html', locals())
    else:
        user = request.user
        return render(request, 'dashboard/index.html')

def profile(request):
    user = request.user
    user_profile = user.userprofile

@login_required
def edit_user(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserFormUpdate(instance=user)

    profile_inline_formset = inlineformset_factory(
        User, UserProfile,
        fields=('githubUsername', 'bio', 'displayName'))
    formset = profile_inline_formset(instance=user)

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
                    return HttpResponseRedirect('/accounts/' + str(user.id))

        return render(request, "account/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied