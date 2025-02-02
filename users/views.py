from cgi import test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from feed.models import Post
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import Profile, FriendRequest, Interest
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .functions import FriendRequestManager
import random
from itertools import chain

User = get_user_model()

@login_required
def users_list(request):
	
	friendsOfFriends = request.user.profile.friendsOfFriends()
	randomUsers = Profile.objects.exclude(user=request.user).exclude(id__in=friendsOfFriends.values("id")).order_by('?')[:10]
	users = list(friendsOfFriends) + list(randomUsers)
	context = {
		'users': users,
		'sent': FriendRequest.objects.filter(from_user=request.user).exclude(to_user__in=request.user.profile.friends.values('id').all())
	}
	return render(request, "users/users_list.html", context)


def friend_list(request):
	p = request.user.profile
	friends = p.friends.all()
	context={
	'friends': friends
	}
	return render(request, "users/friend_list.html", context)

@login_required
def send_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest, created = FriendRequest.objects.get_or_create(
			from_user=request.user,
			to_user=user)
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

@login_required
def cancel_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(
			from_user=request.user,
			to_user=user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

@login_required
def accept_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	if(FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
		request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()
		request_rev.delete()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

@login_required
def delete_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

def delete_friend(request, id):
	user_profile = request.user.profile
	friend_profile = get_object_or_404(Profile, id=id)
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)
	return HttpResponseRedirect('/users/{}'.format(friend_profile.slug))



@login_required
def profile_view(request, slug):
	p = Profile.objects.filter(slug=slug).first()
	u = p.user
	
	context = {
		'u': u,
		'button_status': FriendRequestManager.get_friend_request_status(friend_profile=p, requesting_user=request.user),
		'friends_list': p.friends.all(),
		'sent_friend_requests': FriendRequest.objects.filter(from_user=p.user),
		'rec_friend_requests': FriendRequest.objects.filter(to_user=p.user),
		'post_count': Post.objects.filter(user_name=u).count
	}
	return render(request, "users/profile.html", context)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You can now login!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form':form})

@login_required
def edit_profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('my_profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context ={
		'u_form': u_form,
		'p_form': p_form,
	}
	return render(request, 'users/edit_profile.html', context)

@login_required
def my_profile(request):
	p = request.user.profile
	you = p.user

	context = {
		'u': you,
		'button_status': FriendRequestManager.get_friend_request_status(friend_profile=p, requesting_user=you),
		'friends_list': p.friends.all(),
		'sent_friend_requests': FriendRequest.objects.filter(from_user=you),
		'rec_friend_requests': FriendRequest.objects.filter(to_user=you),
		'post_count': Post.objects.filter(user_name=you).count,
		'interests': p.interests.all()[:5]
	}

	return render(request, "users/profile.html", context)

@login_required
def search_users(request):
	query = request.GET.get('q')
	object_list = User.objects.filter(username__icontains=query)
	context ={
		'users': object_list
	}
	return render(request, "users/search_users.html", context)

@login_required
def delete_interest(request, interest):
	user = request.user
	p = user.profile
	interest = p.interests.get(name=interest)
	if not interest:
		return HttpResponseRedirect('/my-profile/')
	p.interests.remove(interest)
	return HttpResponseRedirect('/my-profile/')

@login_required
def interests(request):
	user = request.user
	p = user.profile
	if request.method == 'POST':
		interest = request.POST.get('interest')
		try:
			interest = Interest.objects.get(name=interest)
		except ObjectDoesNotExist:
			interest = Interest.objects.create(name=interest)
		p.interests.add(interest)
		return HttpResponseRedirect('/my-profile/')
	

	context = {
		'interests': p.interests.all()
	}

	return render(request, "users/interests.html", context)
