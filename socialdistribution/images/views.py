from django.shortcuts import render, render_to_response
from PIL import Image
from images.models import Image
from images.forms import DocumentForm

import logging
logger = logging.getLogger(__name__)


def upload(request):
    """Uploads an image."""
    image_form = DocumentForm()
    return render(request, "uploadImage.html", {'imgForm': image_form})


def create(request):
    """Creates an image."""
    logger.error(request.FILES['thumb'])
    if request.method == 'POST':
        profile = DocumentForm(request.POST, request.FILES)
        DocumentForm.createImage(profile, request.FILES['thumb'])

    return render_to_response("display.html")
