from django.http import HttpRequest, HttpResponse
from .models import *
from .multi_handler import *
from account.models import LoginSession
from datetime import datetime
import json


def get_user_information(request: HttpRequest):
    """
    GET의 query를 통해 session을 전달하면 session을 확인한 후 user 정보를 확인해서 반환한다.\n
    유저 정보는 json의 형태로 나타내진다. 대충 클릭해서 확인해봐라.
    """
    result, content = False, ""
    if request.method == "GET":
        session = request.GET.get("session")
        result, login_session = multi_session(
            LoginSession.objects.filter(session=session))

        if result:
            user = login_session.user

            content = login_session.user.jsonify()

            number = user.numbify()
            seat_number = SeatNumber.objects.filter(number=number)

            content["seat_number"] = seat_number[0] if len(
                seat_number) == 1 else -1
        else:
            content = login_session

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }), content_type="application/json")


def get_user_schedule(request: HttpRequest):
    """
    유저의 세션을 받아서 스케쥴을 반환하는 함수
    """
    result, content = False, ""
    if request.method == "GET":
        session = request.GET.get("session")
        flag, login_session = multi_session(
            LoginSession.objects.filter(session=session))

        if flag:
            result, schedule = multi_schedule(
                UserWeekSchedule.objects.filter(user=login_session.user))
            content = schedule.jsonify() if result else schedule

        else:
            content = login_session

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "schedule": content,
    }), content_type="application/json")


def get_all_class(request: HttpRequest):
    """
    모든 방과후/주문형 강좌 수업에 대한 정보를 제공하는 함수\n
    key가 수업의 id_number이고 value가 infomation이 된다.
    """
    result, content = False, ""
    if request.method == "GET":
        class_list = ClassInformation.objects.all()
        result = True
        content = {}

        for cls in class_list:
            ct = cls.jsonify()
            id = ct['id_number']
            ct.pop('id_number')
            content[id] = ct

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }), content_type="application/json")


def get_today_supervisor(request: HttpRequest):
    """
    오늘 감독 교사 반환하는 함수
    """
    result, content = False, ""
    if request.method == "GET":
        format = "%Y-%m-%d"

        date = datetime.strptime(request.GET.get("date"), format)
        supervisor = Supervisor.objects.filter(date=date)
        print(supervisor)
        result, content = (True, supervisor[0].jsonify()) if len(
            supervisor) >= 1 else (False, "invalid date")

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }), content_type="application/json")


def set_fixed_schedule(request: HttpRequest):
    """
    Todo:
        디자인 애 말 듣고 야자/조퇴랑 방과후/주문형 분리할지 말지를 결정하자고
        그 다음 완성시키기.
    """
    result, content = False, ""
    if request.method == "POST":
        ct = request.content_type

        if 'application/json' in ct:
            data = json.loads(request.body)
            session, fixed_schedule = data['session'], data['fixed']
            res, login_session = multi_session(
                LoginSession.objects.filter(session=session))

            if res:
                user = login_session.user
                result, schedule = multi_schedule(
                    UserWeekSchedule.objects.filter(user=user))

                if result:
                    schedule.mon_fixed = fixed_schedule['mon']
                    schedule.tue_fixed = fixed_schedule['tue']
                    schedule.wed_fixed = fixed_schedule['wed']
                    schedule.thr_fixed = fixed_schedule['thr']
                    schedule.save()

                else:
                    content = schedule

            else:
                result = res
                content = login_session

        else:
            content = "invalid request content_type"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }), content_type="application/json")
