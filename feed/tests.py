from django.test import TestCase, Client
import json
from .models import Post, Comments, Like
from django.contrib.auth.models import User



# Create your tests here.

class FeedCases(TestCase):
    def setUp(self):
        self.client = Client()
        # I generate random strings on this website https://www.thewordfinder.com/random-word-generator
        response = self.client.post('/register/',{
            'username': 'portcommunion', 
            'email': 'wingrider@gmail.com', 
            'password1': 'respondBloating291', 
            'password2': 'respondBloating291'
        })
        
        self.assertEqual(response.status_code, 302) # successful registration redirects client

    def login_test(self):
        self.client.login(username='portcommunion', password='respondBloating291')
        post_response = self.client.post('/post/new/',{
            'description' : 'pepehands', 
            'pic' : 'media/pepehands.png', 
            'tags' : ''
        })
        self.assertEqual(post_response.status_code, 200)

    def search_post(self):
        post_id = Post.objects.filter(description="pepehands").values("id")
        response = self.client.get('/search_posts/', {
            'posts': post_id
        })
        self.assertEqual(response.status_code, 200)

    def test_like_true(self):
        post_id = Post.objects.filter(description="pepehands").values("id")
        response = self.client.get('/like/', {
            'liked':True
        })
        self.assertEqual(response.status_code, 302)

    def test_like_false(self):
        post_id = Post.objects.filter(description="pepehands").values("id")
        response = self.client.get('/like/', {
            'liked':False
        })
        self.assertEqual(response.status_code, 302)

    
class CondRenderTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.LOGIN_ONLY = ["Add New Friends", "Friends", "Profile", "Create Post", "Search posts", "Logout"]
        self.LOGOUT_ONLY = ["Login", "Register"]

    def test_absence(self):
        response = self.client.get('/')
        self.assertContains(response, 'ByteWalk')

        for item in self.LOGIN_ONLY:
            self.assertNotContains(response, item)

        for item in self.LOGOUT_ONLY:
            self.assertContains(response, item)
    
    def test_presence(self):
        self.user = User.objects.create_user('portcommunion', 'portcommunion@example.com', 'respondBloating291')
        self.client.force_login(self.user)

        response = self.client.get('/')
        self.assertContains(response, 'ByteWalk')

        for item in self.LOGOUT_ONLY:
            self.assertNotContains(response, item)
        
        for item in self.LOGIN_ONLY:
            self.assertContains(response, item)