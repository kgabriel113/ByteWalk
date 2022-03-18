from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .models import Profile

# Create your tests here.

class RegistrationTestCase(TestCase):
    def setUp(self):
        c = Client()
        # I generate random strings on this website https://www.thewordfinder.com/random-word-generator
        response = c.post('/register/',{
            'username': 'portcommunion', 
            'email': 'wingrider@gmail.com', 
            'password1': 'respondBloating291', 
            'password2': 'respondBloating291'
        })
        self.assertEqual(response.status_code, 302) # successful registration redirects client

    def test_login(self):
        c = Client()

        response = c.post('/login/',{
            'username': 'portcommunion',
            'password': 'respondBoating291'
        })

        # I'm crying 
        # failed login gives a 200 response smh
        self.assertEqual(response.status_code, 200)

        response = c.post('/login/',{
            'username': 'portcommunion',
            'password': 'respondBloating291'
        })

        self.assertEqual(response.status_code, 302)


class ProfileViewTestCase(TestCase):   
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('portcommunion', 'portcommunion@example.com', 'respondBloating291')
        self.client = Client()
        self.client.force_login(self.user)
        
    
    def test_my_profile(self):
        response = self.client.post('/my-profile/')
        self.assertEqual(response.status_code, 200)
    
    def test_some_profile(self):
        User = get_user_model()
        test_user = User.objects.create_user('fakeuser2', 'a@b.com', 'fakepassword')

        response = self.client.get(f'/users/{test_user.profile.slug}/')
        self.assertEqual(response.status_code, 200)

    
        


