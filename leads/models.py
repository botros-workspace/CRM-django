from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #U need to add the user Auth to the setting in the end (NOTE) 
    #if u want to add other fields to the user class
    #example:  cellPhone = models.CharField(max_length= 15)
    #and remove the pass
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    def __str__(self):
        return self.user.username
    
class Lead(models.Model):
    first_name = models.CharField(max_length= 20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent", on_delete= models.CASCADE)
    def __str__(self):
        return self.first_name + self.last_name
    
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    userProfile = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    #all the Agent fields are defined in the Abstract User Class
    #which is passed through the 'user = models.OneToOneField(User)'
    def __str__(self):
        return self.user.email
    
