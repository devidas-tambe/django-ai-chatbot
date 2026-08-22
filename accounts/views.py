from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {
                "error": "Email already exists"
            })
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        login(request, user)

        return redirect("dashboard")

    return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(
            email=email
        ).first()

        if user is not None:
            from django.contrib.auth import authenticate

            authenticated_user = authenticate(
                username=user.username,
                password=password
            )

            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect("dashboard")

        return render(request, "login.html", {
            "error": "Invalid email or password"
        })

    return render(request, "login.html")
@login_required
def dashboard(request):
    return render(request, "dashboard.html")

def logout_view(request):
    logout(request)
    return redirect("login")