from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    likes = models.ManyToManyField("Post", related_name="likes")
    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE,
                             related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "user_id": self.user_id,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": self.likes.count(),
            "liked_by": [user.id for user in self.likes.all()]
        }
