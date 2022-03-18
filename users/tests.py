from django.test import TestCase, Client
from .forms import UserRegisterForm
from .models import Profile, FriendRequest
import random

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
            'password': 'respondBloating291'
        })


        self.assertEqual(response.status_code, 302)

    
        


class UsersListTestCase(TestCase):
    @staticmethod
    def generate_username():
        characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', '1','2','3','4','5','6','7','8','9','0', 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        username = ''
        for i in range(10):
            username += random.choice(characters)
        return username
    @staticmethod
    def registerUser():
        username = UsersListTestCase.generate_username()
        form = UserRegisterForm({
            'username': username,
            'email': username + '@gmail.com',
            'password1': 'respondBloating291',
            'password2': 'respondBloating291'
            })
        form.save()
        return username

    def register(self):
        self.username = UsersListTestCase.generate_username()

    def registerOtherUsers(self):
        users = []
        for i in range(100):            
            users.append(UsersListTestCase.generate_username())

        self.usernames = users
    
    def makeFriends(self):
        for user in self.usernames + [self.username]:
            # pick 5 random users
            friends = random.sample(self.usernames, 5)
            user1 = Profile.objects.get(user__username=user)
            for friend in friends:
                # make them friends if they aren't already
                user2 = Profile.objects.get(user__username=friend)
                if(user1.friends.filter(user=user2.user).count() == 0):
                    user1.profile.friends.add(user2.profile)
                    user2.profile.friends.add(user1.profile) 
        
    def test_users_list(self):

        #log in
        self.client.login(username='portcommunion', password='respondBloating291')
        response = self.client.get('/users/')
        print(response.content)
        self.assertEqual(response.status_code, 302)

