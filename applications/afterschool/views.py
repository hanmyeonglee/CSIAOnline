from django.http import HttpRequest, HttpResponse
from .models import *
from .multi_handler import *
from account.models import LoginSession
from datetime import datetime, timedelta
from dormitory.views import verify_date, now
from re import fullmatch
import json

from django.views.decorators.csrf import csrf_exempt


def auth_binarify(auth):
    return bin(auth)[2:].ljust(8, '0')


def afterschooluser_default_generator(user: User):
    temp = AfterSchoolUser(
        user=user,
        mon="0/0/0", tue="0/0/0",
        wed="0/0/0", thr="0/0/0",
    )
    temp.save()
    return temp


def userweekschedule_default_generator(afterschool_user: AfterSchoolUser, date: datetime):
    d = date.weekday()
    if d == 0:
        tar = afterschool_user.mon_fixed
    elif d == 1:
        tar = afterschool_user.tue_fixed
    elif d == 2:
        tar = afterschool_user.wed_fixed
    elif d == 3:
        tar = afterschool_user.thr_fixed
    else:
        tar = None

    if not tar == None:
        temp = UserWeekSchedule(
            user=afterschool_user,
            schedule=tar,
            date=date, participate=False,
        )
        temp.save()
        return temp

    else:
        return tar


def seminarroombook_default_generator(date: datetime):
    tmp = SeminarRoomBook(date=date)
    tmp.save()
    return tmp


@csrf_exempt
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


@csrf_exempt
def get_today_supervisor(request: HttpRequest):
    """
    오늘 감독 교사 반환하는 함수
    """
    result, content = False, ""
    if request.method == "GET":
        format = "%Y-%m-%d"

        try:
            date = datetime.strptime(request.GET.get("date"), format)
        except TypeError or ValueError:
            content = "invalid data organization"

        supervisor = Supervisor.objects.filter(date=date)
        result, content = (True, supervisor[0].jsonify()) if len(
            supervisor) == 1 else (False, "invalid date")

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }), content_type="application/json")


@csrf_exempt
def get_afterschooluser_information(request: HttpRequest):
    """
    POST를 통해 session을 전달하면 session을 확인한 후 user 정보를 확인해서 반환한다.\n
    유저 정보는 json의 형태로 나타내진다. 대충 클릭해서 확인해봐라.
    """
    result, content = False, ""
    if request.method == "POST":
        ct = request.content_type

        if 'application/json' in ct:
            flag = True
            try:
                session = json.loads(request.body)['session']
            except:
                content = "invalid data organization"
                flag = False

            if flag:
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

                    seat_number = SeatNumber.objects.filter(
                        number=user.numbify())
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


@csrf_exempt
def get_week_schedule(request: HttpRequest):
    """
    유저의 세션을 받아서 스케쥴을 반환하는 함수
    """
    result, content = False, ""
    if request.method == "POST":
        ct = request.content_type

        if 'application/json' in ct:
            flag = True
            try:
                recv = json.loads(request.body)
                session, date = recv["session"], datetime.strptime(
                    recv["date"], "%Y-%m-%d"
                )
                # 여기서 date는 그 주의 월요일 날짜
                # date가 만약 과거라면 새로운 데이터를 만드는 것은 금지

                verify_date(date, flag=True)

            except Exception as e:
                content = "invalid data organization" + e
                flag = False

            if flag:
                res, login_session = multi_session(
                    LoginSession.objects.filter(session=session))

                if res:
                    user = login_session.user

                    if auth_binarify(user.auth) == "00000000":
                        users = AfterSchoolUser.objects.filter(user=user)
                        content = {
                            "mon": None,
                            "tue": None,
                            "wed": None,
                            "thr": None,
                        }

                        if len(users) == 1:
                            for i, day in enumerate(content.keys()):
                                schedules = UserWeekSchedule.objects.filter(
                                    user=users[0], date=date + timedelta(days=i))

                                if len(schedules) == 1:
                                    content[day] = schedules[0].jsonify()

                                else:
                                    for schedule in schedules:
                                        schedule.delete()
                                    content[day] = userweekschedule_default_generator(
                                        afterschool_user=users[0], date=date + timedelta(days=i)).jsonify()

                            content['message'] = ""

                        else:
                            for usr in users:
                                usr.delete()
                            temp = afterschooluser_default_generator(user=user)

                            for i, day in enumerate(content.keys()):
                                content[day] = userweekschedule_default_generator(
                                    afterschool_user=temp, date=date + timedelta(days=i)).jsonify()

                            content['message'] = "user information is deleted, plase rewrite the fixed_schedule"

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
    }), content_type="application/json")


@csrf_exempt
def set_fixed_schedule(request: HttpRequest):
    """
    POST로 스케쥴이 오면 fixed하게 고정하는 역할
    """
    result, content = False, ""
    if request.method == "POST":
        ct = request.content_type

        if 'application/json' in ct:
            flag = True
            try:
                data = json.loads(request.body)
                print(data)
                session, mon_fixed, tue_fixed, wed_fixed, thr_fixed = \
                    data['session'], data['mon_fixed'], \
                    data['tue_fixed'], data['wed_fixed'], data['thr_fixed'],
            except:
                content = "invalid data organization"
                flag = False

            if flag:
                result, login_session = multi_session(
                    LoginSession.objects.filter(session=session))

                if result:
                    user = login_session.user
                    # afterschoolUser에서 유저를 받아와 그걸 다시 UserWeekSchedule에서 찾아야함

                    if auth_binarify(user.auth) == "00000000":
                        users = AfterSchoolUser.objects.filter(user=user)

                        if len(users) != 1:
                            for user in users:
                                user.delete()
                            afterschool_user = afterschooluser_default_generator(
                                user=user)
                        else:
                            afterschool_user = users[0]

                        afterschool_user.mon_fixed = mon_fixed
                        afterschool_user.tue_fixed = tue_fixed
                        afterschool_user.wed_fixed = wed_fixed
                        afterschool_user.thr_fixed = thr_fixed
                        afterschool_user.save()

                    else:
                        result, content = False, "invalid auth"

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


@csrf_exempt
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
            flag = True
            try:
                recv = json.loads(request.body)
                print(recv)
                session, temp_schedule, date = \
                    recv['session'], recv['temp_schedule'], \
                    datetime.strptime(recv['date'], "%Y-%m-%d")

                n = verify_date(date)

                if recv['date'] == n.strftime("%Y-%m-%d"):
                    if n.hour >= 17:
                        raise RuntimeError()

            except:
                content = "invalid data organization"
                flag = False

            if flag:
                res, login_session = multi_session(
                    LoginSession.objects.filter(session=session))

                if res:
                    user = login_session.user
                    # afterschoolUser에서 유저를 받아와 그걸 다시 UserWeekSchedule에서 찾아야함

                    if auth_binarify(user.auth) == "00000000":
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

                        else:
                            for user in users:
                                user.delete()
                            auser = afterschooluser_default_generator(
                                user=user)
                            schedule = userweekschedule_default_generator(
                                afterschool_user=auser, date=date)

                            content = "user information is deleted, plase rewrite the fixed_schedule"

                        schedule.schedule = temp_schedule
                        schedule.save()

                        result = True

                    else:
                        content = "invalid auth"

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


@csrf_exempt
def get_all_schedule(request: HttpRequest):
    result, content = False, ""

    if request.method == "POST":
        ct = request.content_type

        flag = True
        try:
            recv = json.loads(request.body)
            session, date = \
                recv['session'], datetime.strptime(
                    recv['date'], "%Y-%m-%d")
        except:
            content = "invalid data organization"
            flag = False

        if flag:
            res, login_session = multi_session(
                LoginSession.objects.filter(session=session))

            if res:
                user = login_session.user

                if auth_binarify(user.auth)[7] == "1":
                    students = UserWeekSchedule.objects.filter(date=date)
                    content = []

                    for student in students:
                        seat_number = SeatNumber.objects.filter(
                            number=student.user.user.numbify())
                        tmp = student.user.jsonify()
                        tmp['seat_number'] = seat_number[0] if len(
                            seat_number) == 1 else -1
                        content.append({
                            "student": tmp,
                            "schedule": student.jsonify(),
                        })

                    result = True

                else:
                    content = "invalid auth"

            else:
                content = login_session

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }))


@csrf_exempt
def set_student_participate(request: HttpRequest):
    result, content = False, ""

    if request.method == "POST":
        ct = request.content_type

        if 'application/json' in ct:
            flag = True
            try:
                recv = json.loads(request.body)
                session, date, id = recv['session'], datetime.strptime(
                    recv['date'], "%Y-%m-%d"), recv['id']
            except:
                content = "invalid data organization"
                flag = False

            if flag:
                res, login_session = multi_session(
                    LoginSession.objects.filter(session=session))

                if res:
                    user = login_session.user

                    if auth_binarify(user.auth)[7] == "1":
                        student = UserWeekSchedule.objects.filter(
                            id=id, date=date)

                        if student.exists():
                            st = student[0]
                            st.participate = not st.participate
                            st.save()
                            result = True

                        else:
                            content = "invalid id and date matching"

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


@csrf_exempt
def set_seminar_schedule(request: HttpRequest):
    """
    {
        session: ~,
        schedule: [room1~6_1~3, {
            grade: ~,
            classroom: ~,
            number: ~,
            name: ~,
        } ... ]
    }
    """
    result, content = False, ""
    pattern = r"room[1-6]_[1-3]$"

    if request.method == "POST":
        flag = True
        try:
            recv = json.loads(request.body)
            session, schedule = recv['session'], recv['schedule']
            roomNs, book = schedule[0], schedule[1:]
        except:
            content = "invalid data organization"
            flag = False

        for roomN in roomNs:
            match = fullmatch(pattern, roomN)

        if not match:
            content = "invalid room number"
            flag = False

        n = now()
        bookList = SeminarRoomBook.objects.filter(date=n)

        if bookList.exists():
            bookList = bookList[0]

            for roomN in roomNs:
                if bool(getattr(bookList, roomN)):
                    flag = False
                    content = "already booked room"

        else:
            bookList = seminarroombook_default_generator(date=n)

        if flag:
            res, login_session = multi_session(
                LoginSession.objects.filter(session=session))

            if res:
                user = login_session.user

                if auth_binarify(user.auth) == "00000000":
                    users = []
                    try:
                        for info in book:
                            grade, classroom, number, name = \
                                info['grade'], info['classroom'], \
                                info['number'], info['name']

                            user = User.objects.filter(
                                name=name, grade=grade,
                                classroom=classroom, number=number,
                            )

                            if user.exists():
                                users.append(str(user[0].id))

                            else:
                                content = "invalid user information"
                                flag = False
                                break
                    except:
                        content = "invalid data organization (2)"
                        flag = False

                    if flag:
                        for roomN in roomNs:
                            setattr(bookList, roomN, f"{'/'.join(users)}=0")

                        bookList.save()
                        result = True

                else:
                    content = "invalid auth"

            else:
                content = login_session

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }))


@csrf_exempt
def get_simple_seminar_schedule(request: HttpRequest):
    result, content = False, ""
    if request.method == "GET":
        n = now()
        schedule = SeminarRoomBook.objects.filter(date=n)

        if schedule.exists():
            schedule = schedule[0]

        else:
            schedule = seminarroombook_default_generator(date=n)

        content = schedule.simple_jsonify()
        result = True

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }))
