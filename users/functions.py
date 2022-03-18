from .models import Profile, FriendRequest

# friend_profile: Profile object to check friend request status against
# requesting_user: user (ie from request.user)
def get_friend_request_status(friend_profile, requesting_user):
	if friend_profile not in requesting_user.profile.friends.all():
		if len(FriendRequest.objects.filter(from_user=requesting_user).filter(to_user=friend_profile.user)) == 1:
			return 'friend_request_sent'
		if len(FriendRequest.objects.filter(from_user=friend_profile.user).filter(to_user=requesting_user)) == 1:
			return 'friend_request_received'
		return 'not_friend'
	return 'none'
