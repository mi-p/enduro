from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    number_of_followed = models.PositiveIntegerField(default="0")
    number_of_followers = models.PositiveIntegerField(default="0")

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    time_stamp = models.DateTimeField()
    likes_counter = models.PositiveIntegerField(default="0")

    def __str__(self):
        return f"{self.content[0:10]}... by: {self.author}"

class Follow(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return f"{self.followed.username} <- {self.follower.username}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} -> {self.post.id}"