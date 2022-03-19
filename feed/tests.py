from django.test import TestCase
from django.test import Client
import json
from .models import Post, Comments, Like
from django.contrib.auth.models import User



# Create your tests here.

class SearchPostCase(TestCase):
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
        self.assertEqual(post_response.status_code, 302)

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

    
