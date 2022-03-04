from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

import mimetypes


def is_url_valid(url: str) -> bool:
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return False

    return True


def is_url_valid_image(url: str) -> bool:
    valid_url = is_url_valid(url)
    valid_image = is_url_image(url)
    if valid_url:
        print('valid url: ' + url)

    if valid_image:
        print('valid image: ' + url)

    return is_url_valid(url) and is_url_image(url)


# inspired by MattoTodd on StackOverflow https://stackoverflow.com/a/10543969
def is_url_image(url: str) -> bool:
    mimetype = mimetypes.guess_type(url)
    return (mimetype and mimetype[0] and mimetype[0].startswith('image'))
