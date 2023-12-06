from django.http import HttpRequest, HttpResponse
from .models import User, LoginSession
from .generate_session import generate
from hashlib import sha256
from datetime import datetime, timezone
import json


def hash256(text):
    return sha256(sha256(text).digest()).hexdigest()


def login(request: HttpRequest):
    result, content = False, ""

    if request.method == 'POST':
        ct = request.content_type

        if 'application/json' in ct:
            recv = json.loads(request.body)
            id, pw = recv['id'], hash256(recv['pw'].encode())
            user = User.objects.filter(user_id=id, password=pw)

            if len(user) == 1:
                result = True
                user = user[0]
                for overlap in LoginSession.objects.filter(user=user):
                    overlap.delete()
                content = generate()
                session = LoginSession(
                    user=user, session=content, allot_time=datetime.now(timezone.utc))
                session.save()

            else:
                content = "invalid id or password"

        else:
            content = "invalid data type"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "operation": "login",
        "body": {
            "result": result,
            "content": content,
        }
    }))


def session_confirm(request: HttpRequest):
    result, content = False, ""

    if request.method == "POST":
        ct = request.content_type

        if 'text/plain' in ct:
            session = request.body.decode()

            user_session = LoginSession.objects.filter(session=session)
            if len(user_session) == 1:
                result = True

                content = generate()
                user_session[0].initialize_session(session=content)

            elif len(user_session) > 1:
                content = "invalid session, relogin"

                for one in user_session:
                    one.delete()

            else:
                content = "invalid session, relogin"

        else:
            content = "invalid data type"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "operation": "login",
        "body": {
            "result": result,
            "content": content,
        }
    }))
