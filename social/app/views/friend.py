from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from social.app.models.author import Author


class FriendRequestsListView(generic.ListView):
    context_object_name = "all_friend_requests"
    template_name = "dashboard/friend_requests_list.html"

    def get_queryset(self):
        return self.request.user.profile.incoming_friend_requests.all()

    def post(self, request):
        logged_in_author = self.request.user.profile
        accepted_friend_requests = request.POST.getlist('accepted_friend_requests')

        for new_friend_id in accepted_friend_requests:
            new_friend = Author.objects.get(id=new_friend_id)
            logged_in_author.accept_friend_request(new_friend)
        logged_in_author.save()

        return HttpResponseRedirect(reverse("app:friend-requests-list"))
