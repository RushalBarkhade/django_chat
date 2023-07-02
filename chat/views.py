from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
import json
from chat.models import User


# Create your views here.


def index(request):

    return render(request, "index.html")


def login(request):

    return render(request, "login.html")


def registration(request):

    return render(request, "registration.html")


def contactList(request):

    return render(request, "index.html")


def room(request, room_name):

    return render(request, "room.html", {"room_name": room_name})


def deleteOtherSessions(request):
    pass


def loginSubmit(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        if email or password:
            user_login = authenticate(email=email, password=password)
            if user_login is not None:
                result = User.objects.get(email=email)
                if not int(result.is_active) and not int(result.is_delete):
                    request['temp_username'] = user_login.get_username()
                    deleteOtherSessions(request)

                    return redirect('/chat')
                else:
                    messages.add_message(
                        request, messages.WARNING, "Warning-invalid login! Please check email and password")
                    return redirect("/login")
            else:
                messages.add_message(
                    request, messages.WARNING, "Warning! Authentication Failed! Try again")
                return redirect("/login")
        else:
            messages.add_message(request, messages.WARNING,
                                 "Warning! Authentication Failed! Try again")
            return redirect("/login")
    except Exception as error:
        messages.add_message(request, messages.WARNING,
                             "Warning! Enter valid email and password")
        return redirect("/login")


def registrationSubmit(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    user_email = request.POST['email']
    user_password = request.POST['password']
    username = user_email
    if request.method == "POST":
        try:
            print("request", request.POST)
            email_exist = User.objects.get(username=user_email)
            messages.add_message(
                request, messages.WARNING, "Warning! This username is already exist")
            print("EXIST", email_exist)
            return redirect("/registration")
        except User.DoesNotExist:

            user_new = User.objects.create(
                username=username, email=user_email)
            user_new.set_password(user_password)
            user_new.firstname = firstname
            user_new.lastname = lastname
            user_new.save()
            print('user', user_new)
            messages.add_message(request, messages.SUCCESS,
                                 "User created successfully")
            return redirect('/chat')
    else:
        messages.add_message(request, messages.WARNING,
                             "Warning! Fill all the field")
        return redirect('/registration')
