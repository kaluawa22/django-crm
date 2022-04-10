from django.db import models
from django.forms import CharField
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Built in User Model


class User(AbstractUser):
    pass
    




class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # function to return string form of agent identifier. Using email for this instance. 
    def __str__(self):
        return self.user.email




class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default = 0)
    agent = models.ForeignKey(Agent, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



