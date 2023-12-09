from account.models import User
from .models import *
from random import randint, choice
from datetime import datetime
from pytz import timezone


def now(flag=False):
    """
    현재 서버 시간을 반환해주는 함수\n
    Args:
        flag -> 분, 초도 같이 출력하는지 여부(같이 출력하면 True, 아니면 False, default = False)
    """
    now = datetime.now(timezone('Asia/Seoul'))
    if not flag:
        return datetime(now.year, now.month, now.day)
    return now


def main01():
    users = User.objects.all()
    for user in users:
        tmp = DormitoryUser(
            user=user,
            gender=choice(["M", "F"]),
            room=randint(100, 999),
            mon_fixed="1", tue_fixed="1", wed_fixed="1", thr_fixed="1",
            last_updated=now()
        )
        tmp.save()
    return "done"


def main02():
    dusers = DormitoryUser.objects.all()
    for duser in dusers:
        tmp = NightUserSchedule(
            user=duser,
            schedule=randint(0, 10),
            date="2023-12-10"
        )
        tmp.save()
    return 'done'
