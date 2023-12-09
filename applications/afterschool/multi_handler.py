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
