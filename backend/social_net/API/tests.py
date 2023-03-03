"""
Provides tests for the endpoints.

These tests verify that the endpoints return the expected JSON data.

Example:
To run these tests, execute the following command from the command line:
    $ python manage.py test
"""

# TODO: Add license, more endpoints.

from django.test import TestCase, Client
from . import models
import datetime
import uuid
import random

# FIXME: tHE THING RUNS EACH TEST INDEPENDANT FROM EACH OTHER BUT THAT'S NOT HOW i WROTE THEM.

# Create your tests here.
class PostEndpointTest(TestCase):
    """
    Contains tests for the Post endpoint. The Post endpoint enables the
    creation, updating and fetching of posts.
    
    These tests verify that the Post endpoint returns the expected JSON data,
    and that the creation and updating of posts works as expected.
    """
    
    LOCAL_NODE_ADDR = 'http://127.0.0.1:8000/'
    
    @classmethod
    def helper_generate_comment_json(cls, etc):
        """
        Helper method for generating JSON data for a comment. Not implemented.
        """
        # TODO
        pass
    
    
    @classmethod
    def helper_generate_author_json(cls, id:str, host=LOCAL_NODE_ADDR,
                                    name='fooBar123', url:str=None,
                                                 github:str=None, img:str=None):
        """
        Helper method for generating JSON data for an author.
        
        Args:
            - id (str): A unique identifier for the author.
                - This is not the full url. The full id (which is the url) will
                    be generated using this parameter.
                - Wrong: helper_generate_author_json(id='http://etc.../[id]', ...)
                - Right: helper_generate_author_json(id='[id]', ...)
            - host (str, optional): The host node for the author. Defaults to
                LOCAL_NODE_ADDR.
            - name (str, optional): The author's display name. Defaults to
                'fooBar123'.
            - url (str, optional): The URL for the author. Defaults to the id
                (but with the bse url).
            - github (str, optional): The author's GitHub URL. Defaults to
                'http://github.com/' + name.
            - img (str, optional): The URL of the author's image. Defaults to
                None, If ommitted, will also be ommitted from the JSON data.
        
        Returns:
            dict: JSON data representing the author.
        """
        
        id = host + f'authors/{id}'
        if not url:
            url = id
        if not github:
            github = 'http://github.com/' + name
        
        author_json = {
            "type":"author",
            "id":id,
            "host":host,
            "displayName":name,
            "url":url,
            "github":github,
        }
        if img:
            author_json['img'] = img

        return author_json
        
    
    @classmethod
    def helper_generate_post_json(cls, id:str, author:dict, date:str,
                                  title='Test Post', src:str=None,
                                  origin:str=None, desc='Test Post Description',
                                  ctype='text/plain', content='Hello World!',
                                  categories:'list[str]'=['test', 'dev'],
                                  count=0, comments:str=None,
                                  commentsrc:dict=None, visibility='PUBLIC',
                                                                unlisted=False):
        """
        Generates a JSON object representing a post.

        Args:
            - id (str): The unique ID of the post. Should not include the base URL.
            - author (dict): A dictionary representing the author of the post.
            - date (str): The publication date of the post in ISO 8601 format.
            - title (str): The title of the post. Defaults to 'Test Post'.
            - src (str, optional): The URL of the original post. Defaults to
                `origin`.
            - origin (str, optional): The URL of the post on this server.
                Defaults to `id` (with the base url included).
            - desc (str, optional): A short description of the post. Defaults to
                'Test Post Description'.
            - ctype (str, optional): The content type of the post. Defaults to
                'text/plain'.
            - content (str, optional): The content of the post. Defaults to
                'Hello World!'.
            - categories (list[str], optional): A list of categories for the
                post. Defaults to ['test', 'dev'].
            - count (int, optional): The number of comments on the post.
                Defaults to 0.
            - comments (str, optional): The URL of the comments section for the
                post. Defaults to `id` (with the base url included) concatenated
                with '/comments'.
            - commentsrc (dict, optional): A dictionary representing the JSON
                comment data. If ommitted, it will also not be present in the
                returned JSON.
            - visibility (str, optional): The visibility of the post. Defaults
                to 'PUBLIC'.
            - unlisted (bool, optional): Whether the post is unlisted. Defaults
                to False.

        Returns:
            A dictionary representing the post.
        """
        
        id = author['id'] + f'/posts/{id}'
        if not origin:
            origin = id
        if not src:
            src = origin
        if not comments:
            comments = id + '/comments'
        
        post_json = {
            "type":"post",
            "title":title,
            "id":id,
            "source":src,
            "origin":origin,
            "description":desc,
            "contentType":ctype,
            "content":content,
            "author":author,
            "categories":categories,
            "count":count,
            "comments":comments,
            "published":date,
            "visibility":visibility,
            "unlisted":unlisted
        }
        if commentsrc:
            post_json["commentsSrc"] = commentsrc
            
        return post_json
    
    author_data = {
        'names': ["john", "emily", "june", "sabastian", "edward", "michael", "bob", "joe", "jessica", "alfred", "mozart"],
        'imageLinks': ["https://pbs.twimg.com/profile_images/949787136030539782/LnRrYf6e_400x400.jpg",
                   "https://cdn.theatlantic.com/media/mt/science/cat_caviar.jpg",
                   "https://umbrellacreative.com.au/wp-content/uploads/2020/01/hide-the-pain-harold-why-you-should-not-use-stock-photos-1024x683.jpg",
                   "https://cdn.discordapp.com/attachments/1062163687529521305/1079886393817432214/image.png",
                   "https://preview.redd.it/o3ptlv2r6d681.jpg?width=640&crop=smart&auto=webp&s=55b318959c4cfd9f9f7c952be401389a7913fe21",
                   "https://i.insider.com/602ee9ced3ad27001837f2ac?width=750&format=jpeg&auto=webp"],
    }
    
    post_data = {
        'titles': ['post1', 'post2', 'post3', 'post4', 'post5', 'post6', 'post7', 'post8', 'post9'],
        'descriptions': ['a','b','c','d','e','f','g'],
        'categories': ['web', 'meme', 'dog pictures', 'cat pictures', 'art', 'anime', '#yummyfood', '#funnyfails'],
        'content': ['a','bBBBBBBBBBBBBBB','c','dDDDDDDD','eEE','f','g'],   # TODO: add images 
    }
    
    @classmethod
    def helper_populate_authors(cls, num=6):
        """
        Populate database with num random authors, return a list of urls, author
        ids, expected json formats
        """
        links = []
        uids = []
        url_mid = '/service/authors/'
        jsons = []
        for i in range(num):
            uid = str(uuid.uuid4())
            uids.push(uid)
            rel_url = url_mid + uid
            url = cls.LOCAL_NODE_ADDR + rel_url
            host = cls.LOCAL_NODE_ADDR
            displayname=random.choice(cls.author_data['names'])
            profileimg=random.choice(cls.author_data['imagLinks'])
            github = 'http://github.com/' + displayname
            links.push(rel_url)
            models.AuthorModel.objects.create(type='author', id=uid, url=url,
                                              host=host, displayName=displayname,
                                              github=github, profileImage=profileimg)
            jsons.push(cls.helper_generate_author_json(uid,host,displayname,url,github,profileimg))
        return links, uids, jsons
    
    
    # TODO: populate with comments too.
    @classmethod
    def helper_populate_posts(cls, uids, num=20):
        """
        Populate database with num random posts, return a list of urls and
        expected json formats.
        """
        links = []
        jsons = []
        for i in range(num):
            random.shuffle(uids)
            author_id = uids[0]
            rel_url = '/service/authors/' + author_id + '/posts'
            url_base = cls.LOCAL_NODE_ADDR + rel_url
            pid = str(uuid.uuid4())
            url = url_base + pid
            content = random.choice(cls.post_data['content'])
            links.push(rel_url)
            try:
                origin = random.choice([url_base, cls.LOCAL_NODE_ADDR + '/service/authors/' + random.choice(uids)])
                source = random.choice([url_base, cls.LOCAL_NODE_ADDR + '/service/authors/' + random.choice(uids)])
            except IndexError:
                origin = url_base
                source = url_base
            description = random.choice(cls.post_data['description'])
            categories = []
            for i in range(random.randint(1,4)):
                categories.push(random.choice(cls.post_data['categories']))
            visibility = random.choice([True, False])
            unlisted = random.choice([True, False])
            ctype = random.choice(['text/markdown', 'text/plain'])
            title = random.choice(cls.post_model['titles'])
            commentslink = url + '/comments'
            models.PostsModel.objects.create(type='post', title=title, id=pid,
                                             source=source, origin=origin,
                                             description=description,
                                             contentType=ctype,
                                             visibility=visibility,
                                             unlisted=unlisted, content=content,
                                             author=author_id, comments=commentslink)
            jsons.push(cls.helper_generate_post_json(pid,author_id, DATE_TODO,
                                                     title, source, origin,
                                                     description, ctype, content,
                                                     categories, 0, commentslink, None, visibility, unlisted))
        return links, jsons
            
                
            
        
        
    
    def setUp(self) -> None:
        """
        Sets up the test case.

        This method populates the db full of authors and posts, as well as setting
        up the client to make HTTP requests.
        """        
        self.author_links, uids, self.author_jsons = self.helper_populate_authors()
        self.post_links, self.post_jsons = self.helper_populate_posts(uids)
        
        self.client = Client()
                 
        
    def test_GET_public_post(self):
        """
        Tests getting a public post.

        This method sends an HTTP GET request to the `posts` endpoint to
        retrieve a public post. It then checks that the response status code is
        200 and that the response JSON matches the expected JSON.
        """
        
        response = self.client.get(self.post_links[0])
        json_data = response.json()
        
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.assertJSONEqual(json_data, self.post_jsons[0],
                                       "response json does not match expected.")
        
    
    def test_PUT(self):
        """
        Test the PUT method which uploads a new post with specified id.

        Upload the JSON representation of the post to the server, then verify
        that the post was successfully uploaded by checking that the status code
        is 200, then verify that the post is correct by sending a GET request
        and comparing the JSON response with what was initially sent in the PUT
        request.
        """
        
        pid = str(uuid.uuid4())
        relative_url = '/service/authors/post_test_author/posts/' + pid
        now = datetime.datetime.now().isoformat()
        new_post_json = self.helper_generate_post_json(pid,
                                                       self.author_jsons[0], now)
        response = self.client.put(relative_url, new_post_json,
                                                             'application/json')
        json_data = self.client.get(relative_url).json()
        
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.assertJSONEqual(json_data, new_post_json, 
                                       "response json does not match expected.")
        
        
    def test_POST_new_post(self):
        """
        Tests the POST method for creating a new post without specifying an id.

        The test generates a JSON object for the new post and sends it to the
        server with a POST request, retrieves the ID generated for the new post
        from the response, then uses it to generate the expected JSON received
        from a request to GET the new post. It then checks that the expected
        JSON matches the actual GET request response.

        The test checks the status code of the response, and whether the JSON
        object returned in the response matches the expected JSON object.
        """
        
        relative_url = '/service/authors/post_test_author/posts/'
        now = datetime.datetime.now().isoformat()
        new_post_json = self.helper_generate_post_json('',
                                                         self.author_jsons[0], now)
        response = self.client.put(relative_url, new_post_json,
                                                             'application/json')
        # Note: It would be handy to have the response contain the generated ID,
        # and this test will assume such.
        relative_url += response.content['id']
        new_post_url = relative_url
        new_post_json = self.helper_generate_post_json(response.content['id'],
                                                         self.author_jsons[0], now)
        json_data = self.client.get(relative_url).json()
        
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.assertJSONEqual(json_data, new_post_json, 
                                       "response json does not match expected.")
    
    
    def test_GET_recent_posts(self):
        """Test GET request to retrieve recent posts by an author."""
        # Assuming recent posts just means all posts ordered most recent first and paginated.
        auth_links, uids, auth_jsons = self.helper_populate_authors(1)
        post_links, post_jsons = self.helper_populate_posts(uids)
        relative_url = '/service/authors/post_test_author/posts/'
        response = self.client.get(relative_url, {'page': 1, 'size': 5})
        json_data = response.json()
        
        expected_json = {
            'type': "posts",
            'items': post_jsons     # XXX: Order may not turn out as expectes. Pay attention to this when you strat testing these tests.
        }
        
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.assertJSONEqual(json_data, expected_json, 
                                       "response json does not match expected.")
        
    
    def test_POST_update_existing(self):
        """Test POST request to update an existing post."""
        # TODO: User must be authenticated.
        auth_links, uids, auth_jsons = self.helper_populate_authors(1)
        post_links, post_jsons = self.helper_populate_posts(uids)
        relative_url = post_links[0]
        now = datetime.datetime.now().isoformat()
        new_post_json = self.helper_generate_post_json(
                            'test_post2', auth_jsons[0], now,
                            'Test Post 2 Updated', ctype='text/markdown',
                                           content='Hello World! *remastered*.')
        response = self.client.post(relative_url, new_post_json,
                                                             'application/json')
        json_data = self.client.get(relative_url).json()
        
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.assertJSONEqual(json_data, new_post_json, 
                                       "response json does not match expected.")
        
        
    def test_DELETE(self):
        """Test DELETE request to delete a post by an author."""
        # TODO: User must be authenticated(?)
        auth_links, uids, auth_jsons = self.helper_populate_authors(1)
        post_links, post_jsons = self.helper_populate_posts(uids)
        response = self.client.delete(post_links[0])
        
        self.assertEqual(response.status_code, 404, "Status code is not 404")
