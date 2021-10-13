from django import template
from .post import post_form

register = template.Library()

@register.inclusion_tag('tagtemplates/modal.html')
def modal(*args, **kwargs):
    return {
            'modal_id': kwargs['id'],
            'modal_type': kwargs['type'],
            'modal_label': kwargs['label'],
            'modal_title': kwargs['title'],
            'submit_btn_text': kwargs['btn'],
        }