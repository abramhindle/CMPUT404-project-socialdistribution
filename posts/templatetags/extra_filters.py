from django import template

register = template.Library()


def zip_lists(a, b):
    return zip(a, b)

def return_first(a):
    return a.first()

register.filter('zip', zip_lists)
register.filter('first', return_first)