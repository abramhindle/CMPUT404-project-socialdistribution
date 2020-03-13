Squawk Documentation
========================

The system only allows GET and POST requests; all other requests will be responded to with an HTTP 405 response

Current API Call Formats: (master)
========================

(will be updated to match social_distribution/sd/urls.py found on the api branch)

    
    auth/register
    auth/logout
    auth/getuser
    auth/edituser/<uuid>
    auth/createpost
    auth/getpost
    auth/deletepost
    auth/getallpost
    posts/<uuid>
    posts/<uuid>/comments
    author/<uuid>/post
    friendrequest
    author/<uuid>/friendrequest
    author/<uuid>/posts
    author/posts
    author/<uuid>
    posts/<uuid>/comment
    author/<uuid>/friends

Current Web-Browser Page Paths: (master)
========================

(will be updated to match social_distribution/sd/urls.py found on the api branch)

    
    /
    /feed
    /login
    /logout
    /search
    /account
    /newpost
    /register
    /notifications

