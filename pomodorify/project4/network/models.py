from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
    title = models.CharField(max_length=80)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default = False)
    pomodoro = models.IntegerField(default=1)
    pomo_counter = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Task {self.id} by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"



class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_following")
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="user_followed")

    def __str__(self):
        return f"{self.user} is following {self.user_follower}"


class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="user_post")
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} liked {self.post} it has {self.likes} likes"

