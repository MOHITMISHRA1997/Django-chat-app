from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver

import json


# Create your models here.

class Chat(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.ForeignKey(User,on_delete=models.CASCADE , related_name='sender')
    recipient = models.ForeignKey(User,on_delete=models.CASCADE , default=None, related_name='reciver')
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True,editable=False)  
    
    def __str__(self) -> str:
        return f'This is chat of {self.name}'


class Group(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    def __str__(self) -> str:
        return self.name
    



class Onlineuser(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    def __str__(self) -> str:
        return str(self.user)
    

class Userprofile(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_img = models.ImageField(default='user_icon.png',upload_to='users_dp/')
    def __str__(self) -> str:
        return str(self.user)
    


#****************************** SIGNALS ******************************


#signals fro online / offline
@receiver(post_save,sender = User)
def create_online(sender,created,instance,**kwargs):
    if created:
        Onlineuser.objects.create(user=instance)

    
#Signals for creating Profile
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Userprofile.objects.create(user=instance)

