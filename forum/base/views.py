from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Topic, Message, Feedback, User
from base.forms import RoomForm, UserForm, FeedbackForm, MyUserCreationForm

# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user= User.objects.get(email=email)
        
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        
        else:
            messages.error(request, 'Entered Username or Password are incorrect')

    context ={'page': page}
    return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('/')

def registerPage(request):
    form= MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
           user= form.save(commit=False)
           user.username = user.username.lower()
           user.save()
           login(request, user)
           return redirect('/')
        
        else:
            messages.error(request, 'An error occured during signing you up')

    context = {'form':form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topic = Topic.objects.all()[0:4]
    room_count = room.count()
    room_message= Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'room':room, 'topic':topic, 'room_count':room_count, 'room_message': room_message}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_message= room.message_set.all().order_by('created')
    participants= room.participants.all()

    if request.method == 'POST':
        room_message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',  pk=room.id)   
    context = {'room':room, 'room_message' : room_message, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user= User.objects.get(id=pk)
    room = user.room_set.all()
    room_message = user.message_set.all()
    topic = Topic.objects.all()
    context={'user': user, 'room': room, 'room_message': room_message, 'topic': topic}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topic = Topic.objects.all()
    if request.method == 'POST':
     form = RoomForm(request.POST)
     topic_name= request.POST.get('topic')
     topic, created = Topic.objects.get_or_create(name=topic_name)

     Room.objects.create(
         host=request.user,
         topic=topic,
         name=request.POST.get('name'),
         description=request.POST.get('description'),
     )
     # if form.is_valid():
     #       room = form.save(commit=False)
     #       room.host = request.user
     #      room.save()
     return redirect('home')
        
    context={'form' : form, 'topic' : topic}
    return render(request, 'base/room_form.html', context )

@login_required(login_url='login')
def updateRoom(request, pk):
    room= Room.objects.get(id=pk)
    form= RoomForm(instance=room)
    topic = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('Service could only be accessed by the original room owner!!!')
    if request.method == 'POST':
        topic_name= request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name= request.POST.get('name')
        room.topic= topic
        room.description= request.POST.get('description')
        room.save()
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #    form.save()
        return redirect('home')
    
    context={'form' : form, 'topic':topic, 'room': room}
    return render(request, 'base/room_form.html', context )

@login_required(login_url='login')
def deleteRoom(request, pk):
    room= Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('Service could only be accessed by the original room owner!!!')
    if request.method == 'POST':
            room.delete()
            return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message= Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('Service could only be accessed by the original room owner!!!')
    if request.method == 'POST':
            message.delete()
            return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
           form.save()
           return redirect('user-profile', pk=user.id)
    context = {'form' : form }
    return render(request, 'base/update-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topic = Topic.objects.filter(name__icontains=q)
    context ={'topic': topic}
    return render(request, 'base/topics.html', context)

def activityPage(request):
    room_message = Message.objects.all()
    context = {'room_message': room_message}
    return render(request, 'base/activity.html', context)

@login_required(login_url='login')
def feedbackPortal(request):
    if request.method =="POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = FeedbackForm()

    context = {'form': form}
    return render(request, 'base/feedback.html', context)


    



