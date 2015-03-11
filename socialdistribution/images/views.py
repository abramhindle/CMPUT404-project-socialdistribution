from django.shortcuts import render, render_to_response
from PIL import Image
from images.models import Image
from images.forms import DocumentForm

import logging
from django.template import RequestContext

logger = logging.getLogger(__name__)


def upload(request):
    """Uploads an image."""
    context = RequestContext(request)
    if request.user.is_authenticated():
        image_form = DocumentForm()
        return render(request, "uploadImage.html", {'imgForm': image_form})
    else:
        return _render_error('login.html', 'Please log in.', context)


def create(request):
    """Creates an image."""
    context = RequestContext(request)
    logger.error(request.FILES['thumb'])
    if request.method == 'POST':
        if request.user.is_authenticated():
            profile = DocumentForm(request.POST, request.FILES)
            DocumentForm.createImage(profile, request.FILES['thumb'])
        else:
            return _render_error('login.html', 'Please log in.', context)

    return render_to_response("display.html")

def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)