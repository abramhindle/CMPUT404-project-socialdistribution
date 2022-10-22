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

API Information
=================
## API Endpoints
| Resource                  | POST                    | GET                           | PUT                                     | DELETE  |
| ------------------------- |:-------------:| -----:| -----:| -----:|
| /api/login/                | Logs in an author | - | - | - |
| /api/register/ | Registers a new author | - | - | - |
| /api/logout/                | Logs out an author  | - | - | - |
| /api/authors/                | Logs out an author [A] | - | - | - |
| /api/authors/<author_id>/                | Retrieves an author's profile [A] | Updates an author's profile [A] | - | - |
| /api/authors/<author_id>/inbox/  [WIP]              | Creates a new inbox item for an author [A]  | - | - | - |
| /api/authors/<author_id>/follow-requests/                | - | Retrives the list of follow requests for an author [A] | - | - |
| /api/authors/<author_id>/followers/                | - | Retrives the list of followers for an author [A] | - | - |
| /api/authors/<author_id>/followers/<foreign_author_id>/                | - | Checks if foreign_author_id is a follower of author_id [A] | Accepts a follow request [A] | Removes a follower [A] |


### Notes
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
// TODO

### Remove a follower
// TODO

### Check if an author is following some other author
// TODO

### Retrieve a list of all the followers for an author
// TODO


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
