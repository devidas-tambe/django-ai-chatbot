from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"), 
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("chat/", views.chat, name="chat"), 
    path("new_chat/", views.new_chat, name="new_chat"),
    path("chat/<int:conversation_id>/", views.chat_conversation,name="chat_conversation"),
    path("chat/<int:conversation_id>/rename/",views.rename_chat, name="rename_chat"),

    path("chat/<int:conversation_id>/delete/",views.delete_chat,name="delete_chat"),
]
