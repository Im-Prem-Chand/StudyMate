from django.db import models
from django.contrib.auth.models import AbstractUser

#custom user model
class User(AbstractUser):
    name = models.CharField(max_length=20, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")
    #Assinging the email to username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

class Topic(models.Model):
    name = models.CharField(max_length=200)
    # this func returns name value when Topic class is accessed
    def __str__(self):
        return self.name 

class Room(models.Model):
    #storing 'user'
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #accessing topic names from the Topic class
    #SET_NULL- when topic is deleted, data related to topic still stays in db
    topic = models.ForeignKey(Topic , on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.CharField(null=True, blank=True, max_length=3000)
    participants =models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now = True)
    #auto_now - when ever we save method is called, it records the timestamp
    created = models.DateTimeField(auto_now_add = True)
    # auto_now_add takes time stamp first saved or created even it is saved multiple times

    class Meta:
        ordering = ['-updated','-created']
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #CASCADE - when a room is deleted, actions done in the respective room will be deleted in db also.
    room =  models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50]



