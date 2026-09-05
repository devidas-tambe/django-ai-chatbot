from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Profile, ChatMessage, Conversation
from django.conf import settings
from google import genai
from django.http import JsonResponse 

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
    conversations = Conversation.objects.filter(
        user=request.user
    ).order_by("-created_at")

    chat_messages = ChatMessage.objects.filter(
        user=request.user
    ).order_by("created_at")

    return render(request, "dashboard.html", {
        "conversations": conversations,
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
def new_chat(request):
    conversation = Conversation.objects.create(
        user=request.user,
        title="New Chat"
    )

    return redirect(
        "chat_conversation",
        conversation_id=conversation.id
    )

@login_required
def chat(request):
    if request.method == "POST":

        message = request.POST.get("message")
        conversation_id = request.POST.get("conversation_id")

        if message and conversation_id:

            conversation = Conversation.objects.get(
                id=conversation_id,
                user=request.user
            )

            if conversation.title == "New Chat":
                conversation.title = message[:50]
                conversation.save()

            client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=message
            )

            ai_response = response.text

            ChatMessage.objects.create(
                conversation=conversation,
                user=request.user,
                message=message,
                response=ai_response
            )

            return JsonResponse({
                "success": True,
                "response": ai_response
            })

    return JsonResponse({
        "success": False,
        "error": "Invalid request."
    })

@login_required
def chat_conversation(request, conversation_id):

    conversation = Conversation.objects.get(
        id=conversation_id,
        user=request.user
    )

    chat_messages = ChatMessage.objects.filter(
        conversation=conversation,
        user=request.user
    ).order_by("created_at")

    conversations = Conversation.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "dashboard.html", {
        "conversation": conversation,
        "current_conversation": conversation,
        "conversations": conversations,
        "chat_messages": chat_messages
    })

@login_required
def rename_chat(request, conversation_id):

    conversation = Conversation.objects.get(
        id=conversation_id,
        user=request.user
    )

    if request.method == "POST":
        new_title = request.POST.get("title")

        if new_title:
            conversation.title = new_title[:200]
            conversation.save()

    return redirect(
        "chat_conversation",
        conversation_id=conversation.id
    )

@login_required
def delete_chat(request, conversation_id):

    conversation = Conversation.objects.get(
        id=conversation_id,
        user=request.user
    )

    if request.method == "POST":
        conversation.delete()
        return redirect("dashboard")

    return redirect(
        "chat_conversation",
        conversation_id=conversation.id
    )

def logout_view(request):
    logout(request)
    return redirect("login")
