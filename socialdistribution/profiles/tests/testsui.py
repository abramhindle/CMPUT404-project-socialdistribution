from profiles.models import Author
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from unittest import skip
from profiles.models import Author
from selenium.webdriver.support.wait import WebDriverWait
import time


class ProfilesUITests(StaticLiveServerTestCase):


    @skip("Don't want to test")
    def create_author(self, uuid_id, email, firstName, lastName, displayName, bio, host, github, password):
        return Author.objects.create(id=uuid_id, email=email, firstName=firstName,lastName=lastName,
                                     displayName=displayName, host=host, github=github, password=password)

    @skip("Don't want to test")
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @skip("Don't want to test")
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @skip("Don't want to test")
    # User who didn't have a valid account logins
    def test_cannot_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('hi')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('here')
        self.selenium.find_element_by_xpath('//button[@value="Login"]').click()
        error = self.selenium.find_element_by_class_name("errorlist.nonfield").text
        self.assertEquals('Please enter a correct email and password. Note that both fields may be case-sensitive.', error)

    # User who had a valid account logins
    @skip("Don't want to test")
    def test_can_login(self):
        email = "test@gmail.com"
        firstName = "TestFirst"
        lastName = "TestLast"
        password1 = "testPassword"
        password2 = "testPassword"
        self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
        firstname_input = self.selenium.find_element_by_name("firstName")
        firstname_input.send_keys(firstName)
        lastName_input = self.selenium.find_element_by_name("lastName")
        lastName_input.send_keys(lastName)
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys(email)
        password1_input = self.selenium.find_element_by_name("password1")
        password1_input.send_keys(password1)
        password2_input = self.selenium.find_element_by_name("password2")
        password2_input.send_keys(password2)
        self.selenium.find_element_by_xpath('//button[@value="Register"]').click()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(email)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(password1)
        self.selenium.find_element_by_xpath('//button[@value="Login"]').click()
        redirect = self.selenium.current_url
        self.assertTrue('/stream/' in redirect)

    @skip("Don't want to test")
    def test_can_signup(self):
        email = "test@gmail.com"
        firstName = "TestFirst"
        lastName = "TestLast"
        password1 = "testPassword"
        password2 = "testPassword"
        self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
        firstname_input = self.selenium.find_element_by_name("firstName")
        firstname_input.send_keys(firstName)
        lastName_input = self.selenium.find_element_by_name("lastName")
        lastName_input.send_keys(lastName)
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys(email)
        password1_input = self.selenium.find_element_by_name("password1")
        password1_input.send_keys(password1)
        password2_input = self.selenium.find_element_by_name("password2")
        password2_input.send_keys(password2)
        self.selenium.find_element_by_xpath('//button[@value="Register"]').click()
        redirect = self.selenium.current_url
        self.assertTrue('/accounts/login/' in redirect)
