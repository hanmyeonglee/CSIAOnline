from django.urls import path
from . import views

urlpatterns = [
    path("fix", views.set_fixed_nightschedule, name="fixed_nightschedule"),
    path("temp", views.set_temp_nightschedule, name="temp_nightschedule"),
    path("usernightschedule", views.get_all_nightschedule,
         name="get_nightschedule"),
    path("participate", views.set_student_participate, name="participate"),
]
