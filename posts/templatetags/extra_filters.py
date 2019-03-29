from django import template
from posts.helpers import parse_id_from_url

register = template.Library()


def zip_lists(a, b):
    return zip(a, b)

def return_first(a):
    return a.first()


def parse_user_id(value):
    id = parse_id_from_url(value)
    return id

register.filter('zip', zip_lists)
register.filter('first', return_first)
register.filter('parse_id', parse_user_id)
