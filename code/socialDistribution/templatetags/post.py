from django import template

register = template.Library()

@register.inclusion_tag('tagtemplates/post.html')
def card_post(post):
    return {'post': post}

@register.inclusion_tag('tagtemplates/post_form.html')
def post_form():
    return {}