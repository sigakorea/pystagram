from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    biography = models.TextField(default='')


class UserFollow(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_set')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
        ('from_user', 'to_user'),
    )


def is_follow(self, to_user):
    'self 가 to_user를 follow 하고 있느냐?'
    if self == to_user:
        return False
    return self.following_set.filter(to_user=to_user).exists()
setattr(User, 'is_follow', is_follow)


def follow(self, to_user):
    if self != to_user:
        self.following_set.create(to_user=to_user)
setattr(User, 'follow', follow)


def unfollow(self, to_user):
    if self != to_user:
        self.following_set.filter(to_user=to_user).delete()
setattr(User, 'unfollow', unfollow)

setattr(AnonymousUser, 'is_follow', lambda *args: False)
setattr(AnonymousUser, 'follow', lambda *args: False)
setattr(AnonymousUser, 'unfollow', lambda *args: False)