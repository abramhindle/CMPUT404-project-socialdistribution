from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from author.models import Author
from django.test.utils import setup_test_environment




class AuthorTestCase(TestCase):
    def setUp(self): 
        setup_test_environment()
        user1 = User.objects.create_user(username="myuser1",
                                        password="mypassword")
        user2 = User.objects.create_user(username="myuser2",
                                        password="mypassword")
        user3 = User.objects.create_user(username="results1",
                                        password="mypassword")
        user4 = User.objects.create_user(username="results2",
                                        password="mypassword1")

        author = Author.objects.create(user=user1, github_user='mygithubuser')
        author = Author.objects.create(user=user2, github_user='mygithubuser')

    def test_login_invalid_user_render(self):
        """Testing login for invalid username"""
        c = Client()
        response = c.post('/', {'username': 'nouser',
                                'password': 'mypassword'})

        self.assertNotEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "login.html", msg_prefix='')

    def test_login_invalid_password_render(self):
        """Testing login for wrong password"""
        c = Client()
        response = c.post('/', {'username': 'myuser1',
                                'password': 'wrongpassword'})

        self.assertNotEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "login.html", msg_prefix='')

    def test_login_valid_user_redirect(self):
        """Testing login for valid user"""
        c = Client()
        response = c.post('/', {'username':"myuser1",
                                'password':"mypassword"})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "http://testserver/author/posts/", 
                                status_code=302, target_status_code=200, 
                                msg_prefix='')

    def test_logout_redirect(self):
        """Testing logout for redirection to index"""
        c = Client()
        response = c.get('/author/logout')

        self.assertEqual(response.status_code, 301)


    def test_register_unique_username(self):
        """Testing valid registration inputs with unique username.
        If valid, it will redirect to the '/' aka login page"""
        c = Client()
        response = c.post('/register/', {'userName': "unique",
                                'pwd': "pass",
                                'fName': "name",
                                'lName': "last",
                                'github_username': "account"})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "http://testserver/", 
                                status_code=302, target_status_code=200, 
                                msg_prefix='')


    def test_registration_taken_username(self):
        """testing if username is not unique
        without unique username, response is to render the 
        register.html page. No redirecting"""
        c = Client()
        response = c.post('/register/', {'userName': "myuser1",
                                'pwd': "pass",
                                'fName': "name",
                                'lName': "last",
                                'github_username': "account"})
        self.assertNotEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "register.html", msg_prefix='')

    def test_registration_no_password_render(self):
        """Testing that if no password is inputed
        user is directed to registration page"""
        c = Client()
        response = c.post('/register/', {'userName': "myuser1",
                                'pwd': "",
                                'fName': "name",
                                'lName': "last",
                                'github_username': "account"})
        self.assertNotEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "register.html", msg_prefix='')

    def test_registration_no_username_render(self):
        c = Client()

        response = c.post('/register/', {'userName': "",
                                'pwd': "pwd",
                                'fName': "name",
                                'lName': "last",
                                'github_username': "account"})
        self.assertNotEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "register.html", msg_prefix='')

    def test_registration_create_author(self):
        """upon registration, the user is made into an author"""
        c = Client()
        username = "user"
        response = c.post('/register/', {'userName': username,
                                'pwd': "pwd",
                                'fName': "name",
                                'lName': "last",
                                'github_username': "account"})
        user = User.objects.get(username=username)
        self.assertEqual(len(Author.objects.filter(user=user)), 1)


    def test_search_authors_2_results(self):
        c = Client()
        response = c.post('/author/search/', {'searchValue': "results"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "searchResults.html", msg_prefix='')
        self.assertEqual(response.context['results'], 2)

    def test_search_author_0_result(self):
        c = Client()
        response = c.post('/author/search/', {'searchValue': "nonexist"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "searchResults.html", msg_prefix='')
        self.assertEqual(response.context['results'], 0)
        
    def test_search_empty_string_redirect(self):
        c = Client()
        response = c.post('/author/search/', {'searchValue': ""})

        self.assertEqual(response.status_code, 302)

    def testG_author_connects_user_True(self):
        user = User.objects.get(username="myuser1")
        self.assertEqual(len(Author.objects.filter(user=user)), 1)


    def test_profile_changed_password_redirect(self):
        '''retrieving the profile of the author'''
        c = Client()
        c.login(username='myuser1', password='mypassword')
        user = User.objects.get(username="myuser1")
        author = Author.objects.get(user=user)
        url ='/author/1/'
        response = c.post(url, {'github_username': "string1",
                                        "password":"newPassword",
                                        "first_name":"string3",
                                        "last_name":"string4"})

        self.assertRedirects(response, "http://testserver/", 
                                status_code=302, target_status_code=200, 
                                msg_prefix='')

    def test_profile_changes_saved(self):
        '''edit profile information is saved'''
        c = Client()
        c.login(username='myuser1', password='mypassword')
        user = User.objects.get(username="myuser1")
        author = Author.objects.get(user=user)
        url ='/author/1/'
        response = c.post(url, {'github_username': "string1",
                                        "password":"",
                                        "first_name":"string3",
                                        "last_name":"string4"})

        self.assertTemplateUsed(response, "profile.html")
        self.assertEquals(response.context['github_username'], "string1")
        self.assertEquals(response.context['first_name'], "string3")
        self.assertEquals(response.context['last_name'], "string4")

    def test_profile_get(self):
        """"getting the right information for the author"""
        c = Client()
        c.login(username='myuser1', password='mypassword')
        user = User.objects.get(username="myuser1")
        author = Author.objects.get(user=user)
        url ='/author/1/'
        response = c.get(url, HTTP_ACCEPT="text/html")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
        self.assertEquals(response.context['first_name'], "")
        self.assertEquals(response.context['last_name'], "")
        self.assertEquals(response.context['github_username'], "mygithubuser")


        
   


