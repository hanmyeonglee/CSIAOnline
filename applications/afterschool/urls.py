from django.urls import path

from . import views

urlpatterns = [
    path("information", views.get_user_information, name="user_information"),
    path("schedule", views.get_user_schedule, name="user_schedule"),
    path("all_class", views.get_all_class, name="all_class"),
    path("supervisor", views.get_today_supervisor, name="supervisor"),
    path("fix", views.set_fixed_schedule, name="fix"),
]
