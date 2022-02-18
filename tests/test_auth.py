from django.test import TestCase, Client


class AuthTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_page(self):
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed('auth/login.html')

    def test_signup_page(self):
        res = self.client.get('/signup')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed('auth/signup.html')

    def test_login_redirect(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.get('Location'), '/login')
