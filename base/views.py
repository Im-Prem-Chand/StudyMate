from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


def loginPage(request):
    page = 'login'
    #Even if the webadress has /login, it redirects to home page
    if request.user.is_authenticated:
        return redirect('home')
    
    # get the username and pwd if form method is post
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:    
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Incorrect Username')

        user=authenticate(request, username=username, password=password)
        #If cond to check the correct user or not
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect Username or password')

    context={'page':page}
    return render(request, 'base/login_register.html', context)

# after logout it redirects to home page
def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    # register is key word from the imported UserCreationForm
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            #commit is to get the instance from form but only 'in memory', not in db
            # Before save it you want to make some changes
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save() #save the user
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error Occured during registration')
            
    context = {'form':form,'page':page}
    return render(request, 'base/login_register.html', context)

def homepage(request):
    # Accessing all obj from Room func in models.py
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # filtering the room names using Q Object
    # Q object encapsulates a SQL expression in a Python object that can be used in database-related operations.
    # Using Q objects we can make complex queries with less and simple code
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) 
        | Q(name__icontains=q) 
        | Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    #Filter the home page feed(rooms list) and recent activity based on the room selected topic names
    room_messages = Message.objects.filter(room__topic__name__icontains=q)
    rooms_count = rooms.count
    context = {'rooms':rooms, 'topics':topics, 'rooms_count':rooms_count,'room_messages':room_messages}
    return render(request, 'base/home.html',context)

    # accessing the rooms list in the function
@login_required(login_url='login')
def room(request, pk):
    # Accessing obj by id from Room func in models.py
    room = Room.objects.get(id=pk)
    # sorting the messaged order by created date/time by accessing 
    #all the message obj
    room_messages = room.message_set.all()
    participants = room.participants.all()
    #storing the inputs(user,room and body) receieved from a message
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room=room,
            body=request.POST.get('body')
        )
        #if message added by an user, add user to the participant's list
        room.participants.add(request.user)
        #redirect to the room after adding a msg
        return redirect('room', pk=room.id)

    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request, 'base/room.html',context)

@login_required(login_url='login')
def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    rooms_count = rooms.count
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics,'rooms_count':rooms_count}
    return render(request,'base/profile.html',context)

@login_required(login_url='/login')
def createRoom(request):
    form=RoomForm() #RoomForm() is a class from the forms.py accessing
    #all the fields
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')#after post action, form redirects to home.html
        
    context={'form':form,'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room) #RoomForm() is a class from the forms.py accessing
    #all the fields
    topics = Topic.objects.all()
    if request.user!=room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room=Room.objects.get(id=pk) #accessing by pk value as id
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
            room.delete() #delete function
            return redirect('home')#after post action, form redirects to home.html
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='/login')
def deleteMessage(request, pk):
    message=Message.objects.get(id=pk) #accessing by pk value as id
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
            message.delete() #delete function
            return redirect('home')#after post action, form redirects to home.html
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})