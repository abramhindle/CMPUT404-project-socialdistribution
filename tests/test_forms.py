from django.test import TestCase
import json
from django.urls import reverse
from django.contrib.auth.models import User

from backend.models import Author
from backend.forms import SignUpForm

class SignupForm(TestCase):
    def test_empty_display_name(self):
        form = SignUpForm(data={
            'username': 'test',
            'display_name': '',
            'password1': 'margaret thatcher',
            'password2': 'margaret thatcher',
        })
        self.assertFalse(form.is_valid())
    
    def test_invalid_github_url(self):
        form = SignUpForm(data={
            'username': 'test',
            'display_name': 'test',
            'github_url': "asdfasdf",
            'password1': 'margaret thatcher',
            'password2': 'margaret thatcher',
        })
        self.assertFalse(form.is_valid())
    
    def test_valid_form1(self):
        form = SignUpForm(data={
            'username': 'test',
            'display_name': 'test',
            'password1': 'margaret thatcher',
            'password2': 'margaret thatcher',
        })
        self.assertTrue(form.is_valid())

    def test_valid_form2(self):
        form = SignUpForm(data={
            'username': 'test',
            'display_name': 'test',
            'github_url': 'http://www.github.com/test',
            'password1': 'margaret thatcher',
            'password2': 'margaret thatcher',
        })
        self.assertTrue(form.is_valid())    
