from django.test import TestCase, Client
from django.urls import reverse_lazy


class ViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_redirect(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.get('Location'), reverse_lazy('auth_provider:login'))
