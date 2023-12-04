from .models import LoginSession
import secrets
import string


def session_generate():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))


def generate():
    """
    랜덤한 32bytes의 session을 제작한다.
    이전 session과 중복하지 않은 값이 나올 때까지 반복한다.
    """
    session = session_generate()
    while len(LoginSession.objects.filter(session=session)) != 0:
        session = session_generate()
    return session
