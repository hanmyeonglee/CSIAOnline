from django.http import HttpRequest, HttpResponse
from .models import User, LoginSession
from .generate_session import generate
from afterschool.multi_handler import multi_session
from hashlib import sha256
from datetime import datetime
from pytz import timezone
from afterschool.views import auth_binarify
import json

from django.views.decorators.csrf import csrf_exempt


def hash256(text):
    """
    비밀번호 이중해시
    """
    return sha256(sha256(text).digest()).hexdigest()


@csrf_exempt
def signup(request: HttpRequest):
    """
    회원가입하는 함수\n
    아이디 또는 학번이 이미 존재할 경우 False이다.
    """
    result, content = False, ""

    if request.method == "POST":
        ct = request.content_type

        if 'application/json' in ct:
            flag = True
            try:
                signup = json.loads(request.body)

                name, grade, classroom, number, id, pw = \
                    signup['name'], signup['grade'], signup['classroom'], \
                    signup['number'], signup['id'], signup['pw']
            except:
                content = "invalid data organization"
                flag = False

            if flag:
                if User.objects.filter(grade=grade, classroom=classroom, number=number).exists():
                    content = "exist student number"
                elif User.objects.filter(user_id=id).exists():
                    content = "overlapped id"
                else:
                    temp = User(
                        name=name, grade=grade, classroom=classroom,
                        number=number, auth=0, user_id=id, password=hash256(pw.encode())
                    )
                    temp.save()

                    result = True

        else:
            content = "invalid request content_type"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }))


@csrf_exempt
def login(request: HttpRequest):
    """
    로그인하는 함수, 성공하면 세션을 등록한다.\n
    실패하면 False
    """
    result, content = False, ""

    if request.method == 'POST':
        ct = request.content_type

        if 'application/json' in ct:
            flag = True
            try:
                input_login_information = json.loads(request.body)
                id, pw = input_login_information['id'], hash256(
                    input_login_information['pw'].encode())
            except:
                content = "invalid data organization"
                flag = False

            if flag:
                user = User.objects.filter(user_id=id, password=pw)

                if len(user) == 1:
                    result = True
                    user = user[0]
                    content = generate()
                    session = LoginSession(
                        user=user, session=content, allot_time=datetime.now(timezone('Asia/Seoul')))
                    session.save()

                else:
                    content = "invalid id or password"

        else:
            content = "invalid data type"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }))


@csrf_exempt
def session_confirm(request: HttpRequest):
    """
    세션 확인하는 함수\n
    1. 세션 확인 시 세션 재발급 -> 하나의 기기만 쓰면 ㄱㅊ은데 두 개 이상 사용하면 다중 로그인이 힘듦\n
    2. 세션 재발급 X -> 다중 기기 로그인이 가능함, 그러나 보안상 별로 추천하지는 않음(우선 이걸 선택함)
    """
    result, content = False, ""

    if request.method == "POST":
        ct = request.content_type

        if 'text/plain' in ct:
            flag = True
            try:
                session = request.body.decode()
            except:
                content = "invalid data organization"
                flag = False

            if flag:
                user_session = LoginSession.objects.filter(session=session)
                if len(user_session) == 1:
                    result = True

                    new_session = generate()
                    res = user_session[0].initialize_session(
                        session=new_session)
                    if res:
                        content = {
                            "session": session,
                            "auth": auth_binarify(user_session[0].user.auth),
                        }

                    else:
                        content = "server error"

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
        "result": result,
        "content": content,
    }))


@csrf_exempt
def get_user_information(request: HttpRequest):
    """
    GET의 query를 통해 session을 전달하면 session을 확인한 후 user 정보를 확인해서 반환한다.\n
    유저 정보는 json의 형태로 나타내진다. 대충 클릭해서 확인해봐라.
    """
    result, content = False, ""
    if request.method == "POST":
        ct = request.content_type

        if 'text/plain' in ct:
            try:
                session = request.body.decode()
            except:
                content = "invalid data organization"
                flag = False

            if flag:
                result, login_session = multi_session(
                    LoginSession.objects.filter(session=session))

                if result:
                    content = login_session.user.jsonify()

                else:
                    content = login_session

        else:
            content = "invalid request content_type"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }), content_type="application/json")
