from django.contrib import admin
from service.models import author, post, comment, follow

# Register your models here.

admin.site.register(author.Author)
<<<<<<< HEAD
admin.site.register(post.Post) #we don't need this here, but leaving as comment just in case
=======
admin.site.register(follow.Followers)
#admin.site.register(post.Post) #we don't need this here, but leaving as comment just in case
>>>>>>> 46b21d399abf2a1c3a888dedcd5081359186bde5
#admin.site.register(post.Category)
admin.site.register(comment.Comment)

