from django.shortcuts import redirect
from django.conf import settings

# By Dimit3y (http://stackoverflow.com/users/1234326/dmit3y)
# http://stackoverflow.com/a/21123660/2557554 and licensed under
# CC-BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0/deed.en)
from django.urls import reverse
from django.utils.encoding import iri_to_uri

from dashboard.models import Author


class AuthRequiredMiddleware(object):
    """
    Forces a redirect to the login on all restricted pages.

    Forces a redirect to the home page on accessing the sign-up page while authenticated.
    """

    def process_request(self, request):
        path = request.path_info.lstrip('/')
        if request.user.is_authenticated():
            if any(path == eu for eu in ["accounts/register/"]):
                return redirect(reverse('index'))

            user_profile = Author.objects.get(user_id=request.user.id)

            # Redirect server admins to the admin dashboard
            if user_profile.user.is_staff:
                if not path.startswith('admin') and not path.startswith('service'):
                    return redirect(reverse('admin:index'))
            elif not user_profile.activated:
                # Redirect users that haven't been approved by the server admin
                if not path.startswith('admin') and \
                        not any(path == eu for eu in ["logout/",
                                                      iri_to_uri(reverse('activation_required', args=[])).lstrip('/')]):
                    return redirect(reverse('activation_required', args=[]))
        return None
