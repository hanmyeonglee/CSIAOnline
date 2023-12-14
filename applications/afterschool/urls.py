from django.urls import path

from . import views

urlpatterns = [
    path("all_class", views.get_all_class, name="all_class"),
    path("supervisor", views.get_today_supervisor, name="supervisor"),
    path("afterschool_user_inform", views.get_afterschooluser_information,
         name="afterschool_user_information"),
    path("schedule", views.get_week_schedule, name="user_schedule"),
    path("fix", views.set_fixed_schedule, name="fixed_schedule"),
    path("temp", views.set_schedule, name="temp_schedule"),
    path("all_schedules", views.get_all_schedule, name="get_all_schedules"),
    path("participate", views.set_student_participate, name="student_participate"),
]
