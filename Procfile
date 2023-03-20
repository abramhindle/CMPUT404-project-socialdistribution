release: python manage.py migrate
release: python manage.py createsuperuser --noinput   # Creates a superuser using the values stored
                                                      # in the heroku config vars. Could fail on
                                                      # redployment, which may not be an issue
                                                      # because heroku uses the last release when a
                                                      # release fails. If something is funky though,
                                                      # remember it could be caused by this.
web: gunicorn social_net.wsgi