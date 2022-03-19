from .models import Profile, FriendRequest
import enum

class FriendRequestManager:

    # friend_profile: Profile object to check friend request status against
    # requesting_user: user (ie from request.user)
    def get_friend_request_status(friend_profile: Profile, requesting_user: Profile.user):
        if friend_profile not in requesting_user.profile.friends.all():
            if len(FriendRequest.objects.filter(from_user=requesting_user).filter(to_user=friend_profile.user)) == 1:
                return FriendRequestState.sent
            if len(FriendRequest.objects.filter(from_user=friend_profile.user).filter(to_user=requesting_user)) == 1:
                return FriendRequestState.received
            return FriendRequestState.not_friends
        return FriendRequestState.friends

# convert semantic friend request state to the strings used by the template
class FriendRequestState(enum.Enum):
    sent = 'friend_request_sent'
    received = 'friend_request_received'
    not_friends = 'not_friend'
    friends = 'none'