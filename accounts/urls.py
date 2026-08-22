from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
]