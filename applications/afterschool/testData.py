from account.models import User
from .models import *
from random import randint, choice
from datetime import datetime
from pytz import timezone


def triRandint():
    return f"{randint(0, 10)}/{randint(0, 10)}/{randint(0, 10)}"


def fRandint():
    return f"{randint(0, 1)}{randint(0, 1)}{randint(0, 1)}{randint(0, 1)}"


def main01():
    user_list = User.objects.all()
    for user in user_list:
        date = datetime.now(timezone('Asia/Seoul'))
        date_only = datetime(date.year, date.month, date.day)
        tmp_user = AfterSchoolUser(
            user=user,
            mon_fixed=triRandint(), tue_fixed=triRandint(),
            wed_fixed=triRandint(), thr_fixed=triRandint(),
        )
        tmp_user.save()
        tmp_schedule = UserWeekSchedule(
            user=tmp_user,
            schedule=triRandint(),
            date=date_only, participate=False,
        )
        tmp_schedule.save()


def main02():
    class_names = [
        "Business", "Computer Science/Information Technology", "English",
        "Family and Consumer Science", "Foreign Language",
        "Math", "Performing Arts", "Physical Education", "Science",
        "Social Studies", "Visual Arts", "Vocational Education",
        "Advanced Placement Classes",
    ]
    class_location = [
        "511호", "512호", "513호", "514호",
        "521호", "522호", "523호", "524호",
        "531호", "532호", "533호", "534호",
        "541호", "542호", "543호", "544호",
    ]
    class_day = ["mon", "tue", "wed", "thr"]
    for num in range(0, 11):
        temp = ClassInformation(
            class_name=class_names[num], class_location=class_location[num],
            class_time=f"{choice(class_day)} {fRandint()};",
            class_type=choice(['주문형', '방과후', 'CSMP']), teacher=f"teacher{num}"
        )
        temp.save()


def main03():
    for num in range(4, 15):
        if 9 <= num <= 10:
            continue
        temp = Supervisor(name=f"teacher{num}",
                          date=datetime(2023, 12, num))
        temp.save()
