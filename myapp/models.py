from django.db import models
from django .contrib.auth import get_user_model
import uuid

User=get_user_model()

# Create your models here.
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    id_user=models.IntegerField()
    bio=models.TextField(blank=True)
    profileimg=models.ImageField(upload_to='media',default="blank-profile-picture.png")
    location=models.CharField(max_length=100,blank=True)

    def __str__(self) -> str:
        return self.user.username
    

class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=100)
    image=models.ImageField(upload_to='media')
    caption=models.TextField()
    create_at=models.DateTimeField(auto_now_add=True)
    no_of_likes=models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user
    
class LikePost(models.Model):
    post_id=models.CharField(max_length=500)
    username=models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.username
    
class FollowersCount(models.Model):
    follower=models.CharField(max_length=100)
    user=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user