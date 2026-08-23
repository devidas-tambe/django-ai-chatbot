from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Profile, ChatMessage
from openai import OpenAI
from django.conf import settings

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {
                "error": "This email is already registered."
            })

        user = User.objects.create_user(
            email=email,
            name=name,
            password=password
        )
        Profile.objects.create(user=user)

        login(request, user)

        return redirect("dashboard")

    return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request, "login.html", {
            "error": "Invalid email or password"
        })

    return render(request, "login.html")

@login_required
def dashboard(request):
    chat_messages = ChatMessage.objects.filter(
        user=request.user
    ).order_by("created_at")

    return render(request, "dashboard.html", {
        "chat_messages": chat_messages
    })

@login_required
def profile(request):
    profile = request.user.profile

    return render(request, "profile.html", {
        "profile": profile
    })

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        city = request.POST.get("city")

        request.user.name = name
        request.user.save()

        profile.phone = phone
        profile.city = city
        profile.save()

        return redirect("profile")

    return render(request, "edit_profile.html", {
        "profile": profile
    })

@login_required
def chat(request):
    if request.method == "POST":
        message = request.POST.get("message")

        if message:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            response = client.responses.create(
                model="gpt-5-mini",
                input=message
            )

            ai_response = response.output_text

            ChatMessage.objects.create(
                user=request.user,
                message=message,
                response=ai_response
            )

        return redirect("dashboard")

    return redirect("dashboard")

def logout_view(request):
    logout(request)
    return redirect("login")