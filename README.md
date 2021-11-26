# cmput404-project
Current version is deployed and available on:
https://cmput-404-social-distribution.herokuapp.com/#/

## Setup

> Install the package for backend

```shell
pip install -r requirements.txt
python manage.py migrate
```

> Install the packages for frontend

```
npm install react-bootstrap@next bootstrap@5.1.1 react-router-dom react-router-bootstrap axios react-redux redux-devtools-extension redux-thunk commonmark commonmark-react-renderer
```

> Update frontend before deployment

```
npm run build
```

## Run

If you are running locally make sure that you set `DJANGO_DEFAULT_HOST` to your localhost 

For example, `export DJANGO_DEFAULT_HOST="http://127.0.0.1:8000"`

To deploy the website type the command below in the terminal:
```shell
python manage.py runserver
```

## API Documentation

The API documentation is found on the wiki page [here](https://github.com/cmput404-project-2021fall/CMPUT404-project-socialdistribution/wiki)

# Contributors / Licensing

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Contributors:

- Jihoon Og
- Maristella Jho
- Ivan Zhang
- Dazhi Zhang
- Richard Davidson

# Acknowledgments
This is our collection of references and guides used for the project
## References used
1. Web App General Info: https://www.udemy.com/course/django-with-react-an-ecommerce-website/
2. CSRF Token From Cookies: https://stackoverflow.com/a/50735730
3. CommonMark Rendering on React: https://www.npmjs.com/package/commonmark-react-renderer
4. Creating a signup page: https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
5. How to use Django Field Choices: https://www.geeksforgeeks.org/how-to-use-django-field-choices/
6. BooleanField: Djqngo models: https://www.geeksforgeeks.org/booleanfield-django-models/
7. Serializing with nested objects: https://www.tomchristie.com/rest-framework-2-docs/api-guide/serializers#dealing-with-nested-objects
8. Class based views in Django: https://www.django-rest-framework.org/tutorial/3-class-based-views/
9. Check if a value exists in related fields https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
10. Setting many to many field of an object https://stackoverflow.com/questions/17826629/how-to-set-value-of-a-manytomany-field-in-django
11. Parse a reponse using json.loads https://stackoverflow.com/questions/16877422/whats-the-best-way-to-parse-a-json-response-from-the-requests-library
12. Adding key,value pair to dictionary https://www.tutorialspoint.com/add-a-key-value-pair-to-dictionary-in-python
13. How to specify headers for testing purposes https://stackoverflow.com/questions/31902901/django-test-client-method-override-header
14. How to change the self.client to make test requests as a specific user https://stackoverflow.com/questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
