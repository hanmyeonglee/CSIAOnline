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

        user = login_session.user

        content = user.jsonify() if result else login_session

        number = user.numbify()
        seat_number = SeatNumber.objects.filter(number=number)

        content["seat_number"] = seat_number[0] if len(
            seat_number) == 1 else -1

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
        format = "%Y/%m/%d"

        date = datetime.strptime(request.GET.get("date"), format)
        supervisor = Supervisor.objects.filter(date=date)
        result, content = True, supervisor[0].name if len(
            supervisor) > 1 else False, "invalid date"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }), content_type="application/json")
