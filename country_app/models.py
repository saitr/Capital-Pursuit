from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import *
# Create your models here.

class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=False,null=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False,null=False)

    class Meta:
        abstract = True

# User Model 

class User(AbstractUser):
    username = models.CharField(max_length=150,blank=False,null=False)
    email= models.EmailField(unique=True,blank=False,null=False)
    password = models.CharField(max_length=150,blank=False,null=False)
    otp = models.CharField(max_length=6,blank=True,null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']
    class Meta:
        db_table = 'User'


class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Score of {self.user.username}'
