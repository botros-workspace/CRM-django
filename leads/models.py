from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
    #U need to add the user Auth to the setting in the end (NOTE) 
    #if u want to add other fields to the user class
    #example:  cellPhone = models.CharField(max_length= 15)
    #and remove the pass
    date_added = models.DateField(auto_now_add=True)
    age = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=20)
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)  

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    def __str__(self):
        return self.user.username
    
class Lead(models.Model):
    first_name = models.CharField(max_length= 20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organization = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    agent = models.ForeignKey("Agent",null=True, blank=True, on_delete= models.SET_NULL)
    category = models.ForeignKey("Category",related_name = "leads", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    contacted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    organization = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    #all the Agent fields are defined in the Abstract User Class
    #which is passed through the 'user = models.OneToOneField(User)'
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    organization = models.ForeignKey(UserProfile, on_delete= models.CASCADE)

    def __str__(self):
        return self.name
     
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

post_save.connect(post_user_created_signal, sender= User)