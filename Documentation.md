Squawk Documentation
========================

The website is hosted by Heroku at https://cmput-404.herokuapp.com/ 

Current API Call Formats: (master)
========================
The system only allows GET and POST requests; all other requests will be responded to with an HTTP 405 response
(will be updated to match social_distribution/sd/urls.py found on the api branch)

    
    auth/register               (POST)
    auth/logout                 (GET)
    auth/getuser                (GET)
    auth/edituser/<uuid>        (POST)
    auth/getpost                (GET)
    auth/deletepost             (GET)
    auth/getallpost             (GET)
    posts/<uuid>                (GET)
    posts/<uuid>/comments       (GET)
    author/<uuid>/post          (POST)
    author/<uuid>/posts         (GET)
    author/posts                (GET)
    posts/<uuid>/comment        (POST)

Current Web-Browser Page Paths: (master)
========================

(will be updated to match social_distribution/sd/urls.py found on the api branch)

    
    /               (displays the default explore page)
    /feed           (displays the logged in users)
    /login          (provides a form for the user to login to the system)
    /logout         (logs the currently authenticated user out)
    /search         (displays a concept UI for search functionality (to be implemented))
    /account        (displays the currently authenticated users information)
    /newpost        (provides a form for the user to create a post)
    /register       (provides a form for the user to register as an Author)
    /notifications  (displays a concept UI for the user's notification of requests)

