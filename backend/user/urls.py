from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"/?$", views.Users.as_view()),
    re_path(r"^login/?$", views.LoginView.as_view()),
    re_path(r"^logout/?$", views.LogoutView.as_view()),
    re_path(r"^me/?$", views.Me.as_view()),
    re_path(r"^@<str:username>/?$", views.PublicUser.as_view()),
    re_path(r"^change-password/?$", views.ChangePassword.as_view()),
]
