from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import render,reverse,redirect
from django.contrib.auth import get_user_model


User = get_user_model()

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]

        if auth.authenticate(username=username, password=password): 
            user = auth.authenticate(username=username, password=password)
            print(user)
            auth.login(request, user)
            return redirect('/chat')
        elif auth.authenticate(email=username, password=password):
            print(auth.get_user_model().objects.filter(email=username, password=password).exists())
            auth.login(request, auth.get_user_model().objects.filter(email=username, password=password).exists())
        else:
            return redirect('login')

def index(request):
    return render(request, 'chats/index.html')

def room(request, room_name):
    return render(request, 'chats/room.html', {
        'room_name': room_name
    })
