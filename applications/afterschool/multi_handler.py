from .models import UserWeekSchedule
from django.db.models import Max


def multi_session(sessions):
    """
    LoginSession.objects.filter(session=session)에서 최종 세션을 반환한다.\n
    만약 수가 많으면 다 삭제한다.
    Args:
        sessions -> LoginSession.objects.filter(session=session)
    """
    if len(sessions) == 1:
        return True, sessions[0]
    elif len(sessions) > 1:
        for one in sessions:
            one.delete()
    return False, "invalid session"


def multi_afterschooluser(users, date):
    if len(users) == 1:
        return True, users[0]
    elif len(users) > 1:
        one = max(UserWeekSchedule.objects.filter(
            user=users[0], date=date), key=lambda x: x.date)
        for user in users[1:]:
            temp = max(UserWeekSchedule.objects.filter(
                user=user, date=date), key=lambda x: x.date)
            if temp.date > one.date:
                one = temp
        return True, one
    else:
        return False, "invalid "


'''
def multi_schedule(schedules):
    """
    UserWeekSchedule.objects.filter(user=user)에서 최종 user schedule을 결정한다.
    Args:
        schedules -> UserWeekSchedule.objects.filter(user=user)
    """
    if len(schedules) == 1:
        return True, schedules[0]

    elif len(schedules) > 1:
        recent = schedules[0].mon.date
        final_user = schedules[0]
        for one in schedules[1:]:
            if (one.mon.date - recent).total_seconds() < 0:
                recent = one.mon.date
                final_user.delete()
                final_user = one
        return True, final_user

    else:
        return False, "default"


def multi_afterschool(users):
    """
    AfterSchoolUser.objects.filter(user=login_session.user)에서 user가 다수일떄 user를 결정한다.\n
    Todo:\n
        afterschool 유저가 다수 존재할 때\n
        1. UserWeekSchedule에 있는 유저 빼고는 삭제\n
        2. 다수가 있다면 그 중 가장 최근의 업데이트를 한 date를 가지는 유저를 고름
    """
    if len(users) == 1:
        return True, users[0]
    elif len(users) > 1:
        excepted = []

        for user in users:
            res, schedule = multi_schedule(
                UserWeekSchedule.objects.filter(user=user))
            if res:
                excepted.append(schedule)
 '''
