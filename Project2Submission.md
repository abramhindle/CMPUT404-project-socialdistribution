# Project 2 Submission

1. URL to your publicly available API endpoint: https://social-distribution-t1.herokuapp.com/

2. Valid account credentials for using your application:
   Admin: `username: admin1, password: admin1234`
   Not admin: `username: Remote1, password: remote1234`

   > Basic UmVtb3RlMTpyZW1vdGUxMjM0

3. Example CURL or HTTPIE command for authenticated get POSTS:
   For a specific author: `curl -H "Authorization: Basic UmVtb3RlMTpyZW1vdGUxMjM0" https://social-distribution-t1.herokuapp.com/author/56830ad5f6e347ecb2069bf2cd0f7171/posts/`
   For all public posts: `curl -H "Authorization: Basic UmVtb3RlMTpyZW1vdGUxMjM0" https://social-distribution-t1.herokuapp.com/post-list/`

4. URL to your web service API & documentation:
   https://xuechunqiu.github.io/CMPUT404-project-socialdistribution/

5. The team(s) that you have coordinated with and their endpoints.

   - Team 4 (since they didn't provide enough APIs and their models have not followed the specification exactly, we connected with our own clone system instead): https://social-distribution-t1v2.herokuapp.com/
   - Team 20

## Guide to add a node to your system

1. Find `frontend/src/requests/URL.js`, change

- \_domain (your current domain)
- \_remoteDomain (the domain name of a foreign system)
- \_port (if use localhost, set port to 8000, otherwise leave it empty)
- \_auth (this variable will be put in Authorization Header, so change it to what you need)

2. Change `backend/presentation/Viewsets/URL.py`, change

- domain (your current domain name + port, for example: http://localhost:8000)
- remoteDomain (the domain name of a foreign system)
