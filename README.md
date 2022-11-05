CMPUT404-project-socialdistribution
===================================

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!

Setup
=================
## Backend
1. Move into the backend directory of the repository: `cd backend`
2. Create an start a virtual environment:
```
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```
3. Install dependencies
```
pip install django
pip install djangorestframework
```
4. Run the webserver
```
python manage.py runserver
```
5. Load seed data (note you might need to clear your database first)
```
When asked for authentication enter any of the authors usernames with the password pass123
python manage.py flush   (if your database is not empty)
python manage.py loaddata fixtures/all_data.json
```

### How to Create Seed Data
1. At first, you can create any set of data of your liking through the list API routes or though the frontend.
2. Once you have inserted some meaningful data into your local database, you can dump the data into file fixtures. To do that make sure that you are in the Django project directory (`backend/`) and run the following commands -
```
python manage.py dumpdata webserver --indent 4 > mydata.json
```
This will create a file called `mydata.json` in your current working directory.

3. If you want, you can push this dataset in the `webserver/fixtures` directory of our Github repository.
4. To load this dataset to your local db at a later time, run the following commands -
```
python manage.py flush  # this will clear the current data in your db
python manage.py loaddata mydata.json
```
Now, you're all set!

API Information
=================
## API Endpoints
| Resource                  | POST                    | GET                           | PUT                                     | DELETE  |
| ------------------------- |:-------------:| -----:| -----:| -----:|
| /api/login/                | Logs in an author | - | - | - |
| /api/register/ | Registers a new author | - | - | - |
| /api/logout/                | Logs out an author  | - | - | - |
| /api/authors/                | - | **Retrieves the list of authors [A][R]** | - | - |
| /api/authors/<author_id>/                | **Retrieves an author's profile [A][R]** | Updates an author's profile [A] | - | - |
| /api/authors/<author_id>/inbox/  [WIP]              | **Creates a new inbox item for an author [A][R]**  | Retrieve's an author's inbox [A] | - | - |
| /api/authors/<author_id>/follow-requests/                | - | Retrives the list of follow requests for an author [A] | - | - |
| /api/authors/<author_id>/follow-requests/<foreign_author_id>/                | - | - | - | Decline a follow request[A] |
| /api/authors/<author_id>/followers/                | - | **Retrives the list of followers for an author [A][R]** | - | - |
| /api/authors/<author_id>/followers/<foreign_author_id>/                | - | Checks if foreign_author_id is a follower of author_id [A] | Accepts a follow request [A] | Removes a follower [A] |
| /api/authors/<author_id>/posts/               | Creates a new post for an author [A] | **Retrieves recent posts from an author [A][R]** | - | - |
| /api/authors/<author_id>/posts/<post_id>/                | Update an authors post [A] | **Retrieves an authors post [A][R]** | - | Delete an authors post [A] |

### Notes
- [R] specifies that a remote request can be made to the route. In other words, only those routes marked with [R] accept remote requests. They have also been bolded for ease of navigability.
- [A] specifies that the request must be authenticated
- [WIP] specifies that some features of the endpoint is under development

## Sample Usage
### Register
#### Required fields
- `username`
- `password`
- `password2`
- `display_name`

#### Sample Request
<img width="1130" alt="image" src="https://user-images.githubusercontent.com/43586048/197074885-31cd313d-5d66-489c-81f2-8b69d4d89262.png">


#### Sample Response
```
{
    "username": "author532",
    "display_name": "good_author"
}
```

#### Possible Status Codes
- `201 Created`
- `400 Bad Request`


### Login
#### Required fields
- `username`
- `password`

#### Sample Request
![image](https://user-images.githubusercontent.com/43586048/197075454-33a87648-b4b6-49db-99e9-95591adf7b07.png)

#### Sample Response
```
{
    "message": "Login Success"
}
```

#### Possible Status Codes
- `200 OK`
- `400 Bad Request`
- `401 Unauthorized`


### Logout
#### Required fields
None

#### Sample Request
![image](https://user-images.githubusercontent.com/43586048/197075741-9e0a2256-029d-433e-b457-ae6bb93427e7.png)


#### Sample Response
```
{
    "message": "Successfully Logged out"
}
```

#### Possible Status Codes
- `200 OK`

### Retrieve all profiles on the server
#### Sample Request
<img width="1130" alt="image" src="https://user-images.githubusercontent.com/43586048/197076274-b535b9a4-880e-479a-9302-1c7cb97a9114.png">

#### Sample Response
```
[
    {
        "url": "http://localhost:8000/api/authors/1/",
        "id": 1,
        "display_name": "myuser",
        "profile_image": "",
        "github_handle": ""
    },
    {
        "url": "http://localhost:8000/api/authors/2/",
        "id": 2,
        "display_name": "author_1",
        "profile_image": "",
        "github_handle": ""
    }
]
```

#### Possible Status Codes
- `200 OK`
- `401 Unauthorized`

### Retrieve an author's profile
#### Sample Request
<img width="1130" alt="image" src="https://user-images.githubusercontent.com/43586048/197076848-3d9de2cf-4e7b-4df8-9b69-db1ba8cd222b.png">

#### Sample Response
```
{
    "url": "http://localhost:8000/api/authors/4/",
    "id": 4,
    "display_name": "good_author",
    "profile_image": "",
    "github_handle": ""
}
```

#### Possible Status Codes
- `200 OK`
- `401 Unauthorized`
- `404 Not Found`


### Update an author's profile
#### Sample Request
<img width="1130" alt="image" src="https://user-images.githubusercontent.com/43586048/197077303-4be4bd9a-a978-4e8f-a751-5ce297868b43.png">

#### Sample Response
```
{
    "url": "http://localhost:8000/api/authors/4/",
    "id": 4,
    "display_name": "noob_author",
    "profile_image": "",
    "github_handle": ""
}
```

#### Possible Status Codes
- `200 OK`
- `401 Unauthorized`
- `404 Not Found`

### Send a follow request
#### Sample Request
<img width="1130" alt="image" src="https://user-images.githubusercontent.com/43586048/197077735-cf2ece3b-eb75-491c-b118-37279b37ff53.png">

**Note**: You may wonder why the author `url`s are needed with the request payload. This is needed for project part 2 to differentiate between a local author and a remote one. If an author is a remote one, we will forward the follow request to it's matching remote server.

#### Sample Response
```
{
    "message": "OK"
}
```

#### Possible Status Codes
- `201 Created`
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`
- `409 Conflict`: This can come up when you try to re-send a follow request when the request is still pending

### Retrieve the list of follow requests for an author
#### Sample Request
<img width="1130" alt="image" src="https://user-images.githubusercontent.com/43586048/197078292-978c3672-fee6-419a-ab48-f48604a6bea4.png">

#### Sample Response
```
[
    {
        "url": "http://localhost:8000/api/authors/3/",
        "id": 3,
        "display_name": "myuser",
        "profile_image": "",
        "github_handle": ""
    },
    {
        "url": "http://localhost:8000/api/authors/5/",
        "id": 5,
        "display_name": "author_Z",
        "profile_image": "",
        "github_handle": ""
    }
]
```

#### Possible Status Codes
- `200 OK`
- `401 Unauthorized`
- `404 Not Found`

### Accept a follow request
#### Sample Request
Author with id 4 accepts a follow request of author with id 3 -
<img width="1131" alt="image" src="https://user-images.githubusercontent.com/43586048/197364676-4013d4c9-e3d2-4532-b5d4-98fee42112dd.png">

#### Sample Response
```
{
    "message": "OK"
}
```

#### Possible Status Codes
- `201 Created`
- `400 Bad Request`: This can be returned under a few different circumstances - when a matching follow request does not exist, when valid request payload is not given, or when an authors try to follow themselves
- `401 Unauthorized`
- `404 Not Found`


### Decline a follow request
#### Sample Request
<img width="1134" alt="image" src="https://user-images.githubusercontent.com/43586048/198464624-9e99bc8b-a30a-49a0-8030-b64a751c7f5d.png">

#### Sample Response
```
{
    "message": "Follow request declined"
}
```

#### Possible Status Codes
- `200 OK`: means follow request was declined
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`: can be returned when a matching follow request does not exist


### Remove a follower
#### Sample Request
<img width="1134" alt="image" src="https://user-images.githubusercontent.com/43586048/198466108-f7fde988-9542-4b25-82e7-bc4ac096f88d.png">


#### Sample Response
```
{
    "message": "follower removed"
}
```

#### Possible Status Codes
- `200 OK`
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`: this can be returned when a matching follower can't be found

### Check if an author is following some other author
#### Sample Usage
<img width="1131" alt="image" src="https://user-images.githubusercontent.com/43586048/197365074-6dee55b0-600c-46c1-a3c7-291ae3e07779.png">

#### Sample Response
```
{
    "message": "3 is not a follower of 4"
}
```

**Note:** We can update the response messages over time if requested.

#### Possible Status Codes
- `200 OK`: this is returned when a matching follower specified by the resource url was found.
- `401 Unauthorized`
- `404 Not Found`: this is returned when a matching follower is not found

### Retrieve a list of all the followers for an author
#### Sample Usage
Retrieve the list of followers for author_id 4 -
<img width="1131" alt="image" src="https://user-images.githubusercontent.com/43586048/197365185-7183f1f8-755f-4739-8440-5f0a495e6f7a.png">

#### Sample Response
```
[
    {
        "url": "http://localhost:8000/api/authors/3/",
        "id": 3,
        "display_name": "myuser",
        "profile_image": "",
        "github_handle": ""
    },
    {
        "url": "http://localhost:8000/api/authors/5/",
        "id": 5,
        "display_name": "author_Z",
        "profile_image": "",
        "github_handle": ""
    }
]
```

#### Possible Status Codes
- `200 OK`
- `401 Unauthorized`
- `404 Not Found`

### Retrieve an author's inbox
#### Sample Usage
Retrieve the inbox of author with id 3 -
![image](https://user-images.githubusercontent.com/43586048/197410090-66eba6cd-74ed-48d5-a41d-83e2c0569c50.png)

#### Sample Response
```
[
    {
        "sender": {
            "url": "http://localhost:8000/api/authors/4/",
            "id": 4,
            "display_name": "noob_author",
            "profile_image": "",
            "github_handle": ""
        },
        "type": "follow"
    },
    {
        "author": {
            "url": "http://localhost:8000/api/authors/4/",
            "id": 4,
            "display_name": "noob_author",
            "profile_image": "",
            "github_handle": ""
        },
        "created_at": "2022-10-23T03:25:09.184425Z",
        "edited_at": null,
        "title": "Post 1",
        "description": "Sample description",
        "source": "",
        "origin": "",
        "unlisted": false,
        "content_type": "text/plain",
        "content": "What's up people?",
        "visibility": "FRIENDS",
        "type": "post"
    }
]
```

Notes:
- The `type` field will be present in each inbox item. This specifies the type of the inbox. Possible values: `"post"` for a new post, `"follow"` for a follow request

#### Possible Status Codes
- `200 OK`
- `401 Unauthorized`
- `404 Not Found`


### Retrieve a list of all the posts for an author
#### Sample Usage
Retrieve the list of posts for author id 5 -
<img width="1131" alt="image" src="https://user-images.githubusercontent.com/77307203/197422040-7f02808a-3dc8-4bd8-b441-b0d01b680d4d.png">

#### Sample Response
```
[
    {
        "author": {
            "url": "http://localhost:8000/api/authors/5/",
            "id": 5,
            "display_name": "myuser",
            "profile_image": "",
            "github_handle": ""
        },
        "created_at": "2022-10-22T05:06:49.477100Z",
        "edited_at": "2022-10-22T23:27:41.589319Z",
        "title": "my first post!",
        "description": "Hello world",
        "source": "",
        "origin": "",
        "unlisted": false,
        "content_type": "text/plain",
        "content": "change the content",
        "visibility": "PUBLIC"
    }

]
```

#### Possible Status Codes
- `200 OK`
- `401 Unauthorized`
- `404 Not Found`

### Create a new post
#### Sample Usage
Retrieve the list of posts for author id 5 -
<img width="1131" alt="image" src="https://user-images.githubusercontent.com/77307203/197423346-6aa79f0b-f4f0-4986-85c8-1e29b1467ef1.png">

#### Sample Response
```
[
   {
    "title": "My first post",
    "description": "My first post",
    "unlisted": false,
    "content": "some content",
    "visibility": "PUBLIC",
    "content_type": "text/plain"
    }
]
```

#### Possible Status Codes
- `201 Created`
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`

### Retrieve an authors post
#### Sample Usage
Retrieve the post for author id 5 with post id 55 -
<img width="1131" alt="image" src="https://user-images.githubusercontent.com/77307203/197423796-b0b13176-5ce1-4baa-808e-5e489251e0d5.png">


#### Sample Response
```
[
   {
    "author": {
        "url": "http://127.0.0.1:8000/api/authors/5/",
        "id": 5,
        "display_name": "user123",
        "profile_image": "",
        "github_handle": "user"
    },
    "created_at": "2022-10-22T05:06:49.477100Z",
    "edited_at": "",
    "title": "new Title",
    "description": "Hello world",
    "source": "",
    "origin": "",
    "unlisted": false,
    "content_type": "text/plain",
    "content": "change the content",
    "visibility": "PUBLIC"
    }
]
```

#### Possible Status Codes
- `200 OK`
- `401 Unauthorized`
- `404 Not Found`
- `400 Bad Request`

### Update an authors post
#### Sample Usage
Update the post for author id 5 with post id 55 -
<img width="1131" alt="image" src="https://user-images.githubusercontent.com/77307203/197424158-fd5211d4-79ee-4e1b-bb0c-b8d2585d28be.png">


#### Sample Response
```
[
  {
    "title": "My new post",
    "description": "My new post",
    "unlisted": false,
    "content": "some content"
    }
]
```

#### Possible Status Codes
- `200 OK`
- `401 Unauthorized`
- `404 Not Found`
- `400 Bad Request`

### Delete an authors post
#### Sample Usage
Delete the post for author id 5 with post id 55 -
<img width="1131" alt="image" src="https://user-images.githubusercontent.com/77307203/197424516-02e2fdd2-52d6-4910-a488-b1b05490566c.png">

#### Sample Response
```
[
    {
        "message": "Object deleted!"
    }
]
```
#### Possible Status Codes
- `200 OK`
- `401 Unauthorized`
- `404 Not Found`
- `400 Bad Request`


## Pagination
### Retrieve a paginated list of authors
#### Sample Request
![image](https://user-images.githubusercontent.com/43586048/197662427-57359a86-43d4-4b2b-a7ba-b37f3ede8be1.png)

#### Sample Response
```
{
    "count": 27,
    "next": "http://localhost:8000/api/authors/?page=2&size=5",
    "previous": null,
    "results": [
        {
            "url": "http://localhost:8000/api/authors/1/",
            "id": 1,
            "display_name": "",
            "profile_image": "",
            "github_handle": ""
        },
        {
            "url": "http://localhost:8000/api/authors/2/",
            "id": 2,
            "display_name": "zarif",
            "profile_image": "",
            "github_handle": ""
        },
        {
            "url": "http://localhost:8000/api/authors/3/",
            "id": 3,
            "display_name": "author_0_handle",
            "profile_image": "",
            "github_handle": ""
        },
        {
            "url": "http://localhost:8000/api/authors/4/",
            "id": 4,
            "display_name": "author_1_handle",
            "profile_image": "",
            "github_handle": ""
        },
        {
            "url": "http://localhost:8000/api/authors/5/",
            "id": 5,
            "display_name": "author_2_handle",
            "profile_image": "",
            "github_handle": ""
        }
    ]
}
```

#### Notes
- Use the `page` query parameter to specify the page you would like to fetch. If you just specify the `page` query param without the `size`, a default size of 10 will be used
- Use the `size` query parameter to specify the size of the page. You cannot use this on it's one (you also need to pass the `page` query parameter).
- `count` specifies the total number of records available at this resource
- Send requests to the urls specified in `next` and `prev` to use the pagination

Planning & Design
============
- You can view the [ER model for our app here](https://github.com/zarifmahfuz/project-socialdistribution/blob/master/docs/ERModelv2.png).
- You can view the Figma designs for our UI here.

Deployment
============
If you are added as collaborator on the Heroku app for this project, you should be able to access it here - https://dashboard.heroku.com/apps/social-distribution-14degrees. You are able to do pretty much any administration work on the Heroku app once you're added as a collaborator. Some examples of what you can do -
* You can manually deploy any branch on this repository from the [`Deploy` tab](https://dashboard.heroku.com/apps/social-distribution-14degrees/deploy/github)
* You can ssh into the production container/dyno with the command `heroku ps:exec --dyno=web.1 --app social-distribution-14degrees`
* You can ssh into a one-off (non-production) container/dyno with the command `heroku run bash -a social-distribution-14degrees`

Contributing
============

Send a pull request and be sure to update this file with your name.

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Contributors:

    Karim Baaba
    Ali Sajedi
    Kyle Richelhoff
    Chris Pavlicek
    Derek Dowling
    Olexiy Berjanskii
    Erin Torbiak
    Abram Hindle
    Braedy Kuzma
    Nhan Nguyen 
