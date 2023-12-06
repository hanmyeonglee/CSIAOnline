def multi_session(sessions):
    """
    LoginSession.objects.filter(session=session)에서 최종 세션을 반환한다.
    Args:
        sessions -> LoginSession.objects.filter(session=session)
    """
    if len(sessions) == 1:
        return True, sessions[0]
    elif len(sessions) > 1:
        for one in sessions:
            one.delete()
    return False, "invalid session"


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
