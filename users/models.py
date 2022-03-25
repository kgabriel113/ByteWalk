from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings
from autoslug import AutoSlugField
from django.db.models.expressions import RawSQL

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pics')
	slug = AutoSlugField(populate_from='user')
	bio = models.CharField(max_length=255, blank=True)
	friends = models.ManyToManyField("Profile", blank=True)

	hide_like_counts = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user.username)

	def get_absolute_url(self):
		return "/users/{}".format(self.slug)

	def friendsOfFriends(self):
		# SQL query to get all friends of friends of a user. 
		# Ideally I would do this with a django query set but I am not sure how to do it.
		return Profile.objects.filter(id__in=RawSQL("\
				SELECT f2.to_profile_id FROM users_profile_friends as f1 \
				LEFT JOIN users_profile_friends as f2 ON f1.to_profile_id = f2.from_profile_id \
				WHERE f1.from_profile_id = %s \
			", (self.id,)))

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)

class FriendRequest(models.Model):
	to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
	from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)



