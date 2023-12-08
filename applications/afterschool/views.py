from django.http import HttpRequest, HttpResponse
from .models import *
from .multi_handler import *
from account.models import LoginSession
from datetime import datetime
from pytz import timezone
import json


def afterschooluser_default_generator(user: User):
    temp = AfterSchoolUser(
        user=user,
        mon="0/0/0", tue="0/0/0",
        wed="0/0/0", thr="0/0/0",
    )
    temp.save()
    return temp


def userweekschedule_default_generator(afterschool_user: AfterSchoolUser, date: datetime):
    temp = UserWeekSchedule(
        user=afterschool_user,
        mon=afterschool_user.mon_fixed,
        tue=afterschool_user.tue_fixed,
        wed=afterschool_user.wed_fixed,
        thr=afterschool_user.thr_fixed,
        date=date, participate=False,
    )
    temp.save()
    return temp


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

        try:
            date = datetime.strptime(request.GET.get("date"), format)
            supervisor = Supervisor.objects.filter(date=date)
            result, content = (True, supervisor[0].jsonify()) if len(
                supervisor) == 1 else (False, "invalid date")
        except TypeError and ValueError:
            content = "invalid date format"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }), content_type="application/json")


def get_afterschooluser_information(request: HttpRequest):
    """
    GET의 query를 통해 session을 전달하면 session을 확인한 후 user 정보를 확인해서 반환한다.\n
    유저 정보는 json의 형태로 나타내진다. 대충 클릭해서 확인해봐라.
    """
    result, content = False, ""
    if request.method == "POST":
        ct = request.content_type

        if 'text/plain' in ct:
            # 여기서 session key가 없으면 오류, 이거 예외처리 해놓기
            session = request.body.decode()
            result, login_session = multi_session(
                LoginSession.objects.filter(session=session))

            if result:
                user = login_session.user
                users = AfterSchoolUser.objects.filter(user=user)

                if len(users) == 1:
                    content = users[0].jsonify()

                else:
                    content = afterschooluser_default_generator(
                        user=user).jsonify()

                seat_number = SeatNumber.objects.filter(number=user.numbify())
                content["seat_number"] = seat_number[0] if len(
                    seat_number) == 1 else -1

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


def get_afterschooluser_schedule(request: HttpRequest):
    """
    유저의 세션을 받아서 스케쥴을 반환하는 함수
    """
    result, content = False, ""
    if request.method == "POST":
        ct = request.content_type

        if 'application/json' in ct:
            recv = json.loads(request.body)
            session, date = recv["session"], datetime.strptime(
                recv["date"], "%Y-%m-%d")

            res, login_session = multi_session(
                LoginSession.objects.filter(session=session))

            if res:
                user = login_session.user
                users = AfterSchoolUser.objects.filter(user=user)

                if len(users) == 1:
                    schedules = UserWeekSchedule.objects.filter(
                        user=users[0], date=date)

                    if len(schedules) == 1:
                        result, content = True, schedules[0].jsonify()

                    else:
                        for schedule in schedules:
                            schedule.delete()
                        userweekschedule_default_generator(
                            afterschool_user=users[0], date=date)
                        content = "server error, rewrite the informations"

                else:
                    for usr in users:
                        usr.delete()
                    temp = afterschooluser_default_generator(user=user)
                    userweekschedule_default_generator(
                        afterschool_user=temp, date=date)
                    content = "server error, rewrite the informations"

            else:
                content = login_session

        else:
            content = "invalid request content_type"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "schedule": content,
    }), content_type="application/json")


def set_fixed_schedule(request: HttpRequest):
    """
    POST로 스케쥴이 오면 fixed하게 고정하는 역할
    """
    result, content = False, ""
    if request.method == "POST":
        ct = request.content_type

        if 'application/json' in ct:
            data = json.loads(request.body)
            session, fixed_schedule = data['session'], data['fixed_schedule']
            result, login_session = multi_session(
                LoginSession.objects.filter(session=session))

            if result:
                user = login_session.user
                # afterschoolUser에서 유저를 받아와 그걸 다시 UserWeekSchedule에서 찾아야함
                users = AfterSchoolUser.objects.filter(user=user)

                if len(users) != 1:
                    for user in users:
                        user.delete()
                    afterschool_user = afterschooluser_default_generator(
                        user=user)
                else:
                    afterschool_user = users[0]

                afterschool_user.mon_fixed = fixed_schedule['mon_fixed']
                afterschool_user.tue_fixed = fixed_schedule['tue_fixed']
                afterschool_user.wed_fixed = fixed_schedule['wed_fixed']
                afterschool_user.thr_fixed = fixed_schedule['thr_fixed']
                afterschool_user.save()

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


def set_schedule(request: HttpRequest):
    """
    고정된 건 아니고 그날그날 신청사항을 받음
    Todo:
        날짜 제한 제대로 하기
    """
    result, content = False, ""
    if request.method == "POST":
        ct = request.content_type

        if 'application/json' in ct:
            data = json.loads(request.body)
            session, temp_schedule, date = \
                data['session'], data['temp_schedule'], \
                datetime.strptime(data['date'], "%Y-%m-%d")

            res, login_session = multi_session(
                LoginSession.objects.filter(session=session))

            if res:
                user = login_session.user
                # afterschoolUser에서 유저를 받아와 그걸 다시 UserWeekSchedule에서 찾아야함
                users = AfterSchoolUser.objects.filter(user=user)

                if len(users) == 1:
                    afterschool_user = users[0]
                    schedules = UserWeekSchedule.objects.filter(
                        user=afterschool_user, date=date)

                    if len(schedules) != 1:
                        for schedule in schedules:
                            schedule.delete()
                        schedule = userweekschedule_default_generator(
                            afterschool_user=afterschool_user, date=date)

                    else:
                        schedule = schedules[0]

                    schedule.mon = temp_schedule['mon']
                    schedule.tue = temp_schedule['tue']
                    schedule.wed = temp_schedule['wed']
                    schedule.thr = temp_schedule['thr']
                    schedule.save()

                    result = True

                else:
                    for user in users:
                        user.delete()
                    afterschooluser_default_generator(user=user)
                    content = "server error, rewrite the informations"

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


def get_all_schedule(request: HttpRequest):
    result, content = False, ""

    if request.method == "POST":
        ct = request.content_type

        if 'application/json' in ct:
            recv = json.loads(request.body)
            session, date = \
                recv['session'], datetime.strptime(recv['date'], "%Y-%m-%d")

            res, login_session = multi_session(
                LoginSession.objects.filter(session=session))

            if res:
                user = login_session.user

                if user.auth == 1:
                    students = UserWeekSchedule.objects.filter(date=date)
                    content = []

                    for student in students:
                        content.append({
                            "student": student.user.jsonify(),  # 여기 정보에 seat_number 있어야 하는데;
                            "schedule": student.jsonify(),
                        })

                    result = True

                else:
                    content = "invalid auth"

            else:
                content = login_session

        else:
            content = "invalid request content_type"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }))


def set_student_participate(request: HttpRequest):
    result, content = False, ""

    if request.method == "POST":
        ct = request.content_type

        if 'application/json' in ct:
            recv = json.loads(request.body)
            session, date, id = recv['session'], datetime.strptime(
                recv['date'], "%Y-%m-%d"), recv['id']

            res, login_session = multi_session(
                LoginSession.objects.filter(session=session))

            if res:
                user = login_session.user

                if user.auth == 1:
                    student = UserWeekSchedule.objects.filter(id=id, date=date)

                    if len(student) == 1:
                        student[0].participate = not student[0].participate
                        student[0].save()
                        result = True

                    else:
                        content = "server error, reboot the website"

                else:
                    content = "invalid auth"

            else:
                content = login_session

        else:
            content = "invalid request content_type"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }))
