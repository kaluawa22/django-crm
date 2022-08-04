from django.db import models
from django.forms import CharField
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.

# Built in User Model


class User(AbstractUser):
    is_organizor = models.BooleanField(default = True)
    is_agent = models.BooleanField(default = True)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    # function to return string form of agent identifier. Using email for this instance. 
    def __str__(self):
        return self.user.email




class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default = 0)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete = models.SET_NULL)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    


    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Category(models.Model):
    # New, Contacted, Converted, Unconververted created in Admin
    name = models.CharField(max_length=20)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# creates corresponding User Profile when user is created. Only If created returns TRUE
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# SIGNALS for when user is created. 
post_save.connect(post_user_created_signal, sender=User)