from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/chat/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid username.")
            return redirect("/login/")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid password.")
            return redirect("/login/")
        else:
            login(request, user)
            return redirect("/chat-list/")

    return render(request, "login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("/chat-list/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already taken.")
            return redirect("/register/")

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        messages.info(request, "User created successfully.")
        return redirect("/login/")
    return render(request, "register.html")


def logout_page(request):
    logout(request)
    return redirect("/login/")
