from django.shortcuts import redirect
from django.conf import settings


# By Dimit3y (http://stackoverflow.com/users/1234326/dmit3y)
# http://stackoverflow.com/a/21123660/2557554 and licensed under
# CC-BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0/deed.en)
from django.urls import reverse
from django.utils.encoding import iri_to_uri

from dashboard.models import UserProfile


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
            if not any(path == eu for eu in ["", "login/", "accounts/register/", "admin/"]):
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))  # or http response
        else:
            if any(path == eu for eu in ["accounts/register/"]):
                return redirect('/')  # or http response

            userProfile = UserProfile.objects.get(user_id=request.user.id)
            print(iri_to_uri(reverse('activation_required', args=[])))
            if(userProfile.activated == False):
                if not path.startswith('admin') and \
                        not any(path == eu for eu in ["logout/",
                                                      iri_to_uri(reverse('activation_required', args=[])).lstrip('/')]):
                    return redirect(reverse('activation_required', args=[]))
        return None
