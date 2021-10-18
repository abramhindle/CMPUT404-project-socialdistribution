from django import template
from .post import post_form

register = template.Library()

# Django Software Foundation, "Custom Template tags and Filters", 2021-10-10
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#inclusion-tags
@register.inclusion_tag('tagtemplates/modal.html')
def modal(*args, **kwargs):
    return {
            'modal_id': kwargs['id'],
            'modal_type': kwargs['type'],
            'modal_label': kwargs['label'],
            'modal_title': kwargs['title'],
            'submit_btn_text': kwargs['btn'],
        }