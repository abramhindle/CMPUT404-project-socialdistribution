from django import template

register = template.Library()

# Django Software Foundation, "Custom Template tags and Filters", 2021-10-10
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#inclusion-tags
@register.inclusion_tag('tagtemplates/author.html')
def card_author(*args, **kwargs):
    """
        Returns info relevant to an author comment 
    """
    author = kwargs['author']
    author_type = kwargs['author_type']
    profile_card = kwargs['profile_card']
    comment_card = None
    comment = None
    is_following = False
    request_sent = False
    is_friend = False
    author_is_user = False

    if 'comment_card' in kwargs:
        comment_card = kwargs['comment_card']
        comment = kwargs['comment']

    if profile_card:
        curr_user = kwargs['curr_user']
        is_following = author.has_follower(curr_user)
        request_sent = author.inbox.has_req_from(curr_user)
        is_friend = curr_user.is_friends_with(author)
        author_is_user = author.id == curr_user.id


    return {
        'author': author,
        'author_type': author_type,
        'profile_card': profile_card,
        'comment_card': comment_card,
        'comment': comment,
        'is_following': is_following,
        'request_sent': request_sent,
        'is_friend': is_friend,
        'author_is_user': author_is_user
    }