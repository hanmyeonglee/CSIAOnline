from django.urls import path

from . import views

urlpatterns = [
    # link/account/login
    path("login", views.login, name="login"),
    path("session", views.session_confirm, name="session"),
    path("signup", views.signup, name="signup"),
    path("tlogin", views.tlogin, name="tlogin"),
    path("user_inform", views.get_user_information, name="user_information"),
]
