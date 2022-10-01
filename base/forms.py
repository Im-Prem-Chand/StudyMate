from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

class MyUserCreationForm(UserCreationForm):
    
    class Meta:
        model=User
        fields= ['name', 'username', 'email', 'password1', 'password2']



class RoomForm(ModelForm):
    class Meta:
        model=Room # assigning 'Room' table or class from the models(db)
        fields='__all__' # assigning all the fields in 'Room' table or class
        exclude =['host','participants'] #excludes mentionsed list in the front-end view

class UserForm(ModelForm):
    class Meta:
        model=User # assigning 'User' table or class from the models(db)
        fields = ['avatar', 'name', 'username', 'email', 'bio']        
