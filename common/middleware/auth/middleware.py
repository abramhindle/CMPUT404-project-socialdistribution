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
        if not request.user.is_authenticated():
            # Login check by conner.xyz (http://stackoverflow.com/users/2836259/conner-xyz)
            # http://stackoverflow.com/a/40873794/2557554
            # CC-BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0/deed.en)
            if not any(path == eu for eu in ["", "login/",
                                             "accounts/register/",
                                             "accounts/password/reset/",
                                             "admin/"]):
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))  # or http response
        else:
            if any(path == eu for eu in ["accounts/register/"]):
                return redirect('/')  # or http response

            user_profile = Author.objects.get(user_id=request.user.id)

            # Redirect server admins to the admin dashboard
            if user_profile.user.is_staff:
                if not path.startswith('admin'):
                    return redirect(reverse('admin:index'))

            # Redirect users that haven't been approved by the server admin
            if not user_profile.activated:
                if not path.startswith('admin') and \
                        not any(path == eu for eu in ["logout/",
                                                      iri_to_uri(reverse('activation_required', args=[])).lstrip('/')]):
                    return redirect(reverse('activation_required', args=[]))
        return None
