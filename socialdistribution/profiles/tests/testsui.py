from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

class ProfilesUITests(StaticLiveServerTestCase):

    def create_author(self, uuid_id, email, firstName, lastName, displayName, bio, host, github, password):
        return Author.objects.create(id=uuid_id, email=email, firstName=firstName,lastName=lastName,
                                     displayName=displayName, host=host, github=github, password=password)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('hi')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('here')
        self.selenium.implicitly_wait(100)
        self.selenium.find_element_by_xpath('//button[@value="Login"]').click()
        error = self.selenium.find_element_by_class_name("errorlist.nonfield").text
        self.assertEquals('Please enter a correct email and password. Note that both fields may be case-sensitive.', error)
