from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    likes = models.ManyToManyField("Post", related_name="liked_by")
    followers = models.ManyToManyField("self", related_name="follow")

    def valid_follow(self, user):
        if self.id == user.id:
            return False
        return True

    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE,
                             related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def liked(self, user):
        if user in self.liked_by.filter(pk=user.id):
            return True
        return False

    def serialize(self, user):
        return {
            "id": self.id,
            "username": self.user.username,
            "user_id": self.user_id,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": self.liked_by.count(),
            "liked_by": [user.id for user in self.liked_by.all()],
            "liked": self.liked(user)
        }
