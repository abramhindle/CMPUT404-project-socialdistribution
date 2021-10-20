from django import template

register = template.Library()

# Django Software Foundation, "Custom Template tags and Filters", 2021-10-10
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#inclusion-tags
@register.inclusion_tag('tagtemplates/post.html')
def card_post(post, author):
    # Delete/Edit
    isAuthor = post.author == author

    # Likes
    isLiked = post.likes.filter(id=author.id).exists()
    likeText = ''
    likes = post.total_likes()
    if isLiked:
        likes -= 1
        if likes >= 2:
            likeText = f'Liked by you and {likes} others'
        elif likes == 1:
            likeText = f'Liked by you and 1 other'
        else:
            likeText = f'Liked by you'
    else:
        likes = post.likes.count()
        if likes > 1:
            likeText = f'Liked by {likes} others'
        elif likes == 1:
            likeText = f'Liked by 1 other'

    return {'post': post, 'isAuthor': isAuthor, 'isLiked': isLiked, 'likeText': likeText}


@register.inclusion_tag('tagtemplates/post_form.html')
def post_form():
    return {}
