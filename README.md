# cmput404-project

### Setup

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

### Run

If you are running locally make sure that you set `DJANGO_DEFAULT_HOST` to your localhost 

> Run the backend

```shell
python manage.py runserver
```

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

## Maristella's References:

1. Web App General Info: https://www.udemy.com/course/django-with-react-an-ecommerce-website/
2. CSRF Token From Cookies: https://stackoverflow.com/a/50735730
3. CommonMark Rendering on React: https://www.npmjs.com/package/commonmark-react-renderer

## Richard's References:
1. For fields with multiple choices in Model https://www.geeksforgeeks.org/how-to-use-django-field-choices/
2. For boolean fields in Model https://www.geeksforgeeks.org/booleanfield-django-models/
3. Knowledge on serializers https://www.tomchristie.com/rest-framework-2-docs/api-guide/serializers#dealing-with-nested-objects
4. Check if a value exists in related fields https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
5. Setting many to many field of an object https://stackoverflow.com/questions/17826629/how-to-set-value-of-a-manytomany-field-in-django
6. Parse a reponse using json.loads https://stackoverflow.com/questions/16877422/whats-the-best-way-to-parse-a-json-response-from-the-requests-library
7. Adding key,value pair to dictionary https://www.tutorialspoint.com/add-a-key-value-pair-to-dictionary-in-python