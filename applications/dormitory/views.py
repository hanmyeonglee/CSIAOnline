from django.http import HttpRequest, HttpResponse
from .models import *
from account.models import *
from afterschool.models import ClassInformation
from afterschool.multi_handler import *
from datetime import datetime, timedelta
from pytz import timezone
import json

from django.views.decorators.csrf import csrf_exempt


def auth_binarify(auth):
    return bin(auth)[2:].ljust(8, '0')


def now(flag=False):
    """
    현재 서버 시간을 반환해주는 함수\n
    Args:
        flag -> 분, 초도 같이 출력하는지 여부(같이 출력하면 True, 아니면 False, default = False)
    """
    now = datetime.now(timezone('Asia/Seoul'))
    if not flag:
        return datetime(now.year, now.month, now.day)
    return now


def verify_date(date: datetime, flag=False):
    n = now(True)
    timez = timezone('Asia/Seoul')
    date = timez.localize(date)

    if flag:
        if date.weekday() != 0:
            raise RuntimeError()

    if date >= datetime(n.year + 1, 2, 1, tzinfo=timez) or date <= datetime(n.year, 2, 28, tzinfo=timez):
        raise RuntimeError()

    if date > n + timedelta(days=21):
        raise RuntimeError()

    return n


def dormitoryuser_default_generator(user: User):
    tmp = DormitoryUser(
        user=user,
        gender="M",
        room=-1,
        mon_fixed="1",
        tue_fixed="1",
        wed_fixed="1",
        thr_fixed="1",
        last_updated=now(),
    )
    tmp.save()
    return tmp


def nightschedule_default_generator(user: DormitoryUser, date: datetime):
    tmp = NightUserSchedule(
        user=user,
        schedule="1",
        date=date,
    )
    tmp.save()
    return tmp


@csrf_exempt
def set_fixed_nightschedule(request: HttpRequest):
    result, content = False, ""
    if request.method == "POST":
        flag = True
        try:
            recv = json.loads(request.body)
            session = recv['session']
            mon_fixed, tue_fixed, wed_fixed, thr_fixed = \
                recv['mon_fixed'], recv['tue_fixed'], recv['wed_fixed'], recv['thr_fixed']
        except:
            content = "invalid data organization"
            flag = False

        if flag:
            res, login_session = multi_session(
                LoginSession.objects.filter(session=session)
            )

            if res:
                user = login_session.user

                if auth_binarify(user.auth) == "00000000":
                    dusers = DormitoryUser.objects.filter(
                        user=user)

                    if dusers.exists():
                        duser = dusers[0]

                    else:
                        duser = dormitoryuser_default_generator(user=user)

                    duser.mon_fixed, duser.tue_fixed, duser.wed_fixed, duser.thr_fixed = \
                        mon_fixed, tue_fixed, wed_fixed, thr_fixed
                    duser.save()

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
    }), content_type="application/json")


@csrf_exempt
def set_temp_nightschedule(request: HttpRequest):
    result, content = False, ""
    if request.method == "POST":
        flag = True
        try:
            recv = json.loads(request.body)
            session, schedule, date = \
                recv['session'], recv['schedule'], \
                datetime.strptime(recv['date'], "%Y-%m-%d")

            n = verify_date(date)

            if recv['date'] == n.strftime("%Y-%m-%d"):
                if int(n.strftime("%H%M")) >= 2150:
                    raise RuntimeError()

        except:
            content = "invalid data organization"
            flag = False

        if flag:
            res, login_session = multi_session(
                LoginSession.objects.filter(session=session)
            )

            if res:
                user = login_session.user

                if auth_binarify(user.auth) == "00000000":
                    dusers = DormitoryUser.objects.filter(user=user)

                    if dusers.exists():
                        duser = dusers[0]

                    else:
                        duser = dormitoryuser_default_generator(user=user)

                    temp_ns = NightUserSchedule.objects.filter(
                        user=duser, date=date)

                    if temp_ns.exists():
                        ns = temp_ns[0]

                    else:
                        ns = nightschedule_default_generator(
                            user=duser, date=date)

                    ns.schedule = schedule
                    ns.save()

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
    }), content_type="application/json")


@csrf_exempt
def get_user_inform(request: HttpRequest):
    result, content = False, ""
    if request.method == "POST":
        flag = True
        try:
            recv = json.loads(request.body)
            session = recv['session']
        except:
            content = "invalid data organization"
            flag = False

        if flag:
            res, login_session = multi_session(
                LoginSession.objects.filter(session=session)
            )

            if res:
                user = login_session.user

                if auth_binarify(user.auth) == "00000000":
                    dusers = DormitoryUser.objects.filter(user=user)

                    if dusers.exists():
                        duser = dusers[0]
                        result, content = True, duser.jsonify()

                    else:
                        duser = dormitoryuser_default_generator(user=user)

                        result, content = True, duser.jsonify()

                else:
                    content = "invalid auth"

            else:
                content = "invalid session"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }), content_type="application/json")


@csrf_exempt
def get_week_nightschedule(request: HttpRequest):
    result, content = False, ""
    if request.method == "POST":
        flag = True
        try:
            recv = json.loads(request.body)
            session, date = \
                recv['session'], datetime.strptime(recv['date'], "%Y-%m-%d")
            # 여기서 date는 그 주의 월요일 날짜
            # date가 만약 과거라면 새로운 데이터를 만드는 것은 금지

            verify_date(date, flag=True)

        except:
            content = "invalid data organization"
            flag = False

        if flag:
            res, login_session = multi_session(
                LoginSession.objects.filter(session=session)
            )

            if res:
                user = login_session.user

                if auth_binarify(user.auth) == "00000000":
                    dusers = DormitoryUser.objects.filter(user=user)
                    content = {
                        'mon': None,
                        'tue': None,
                        'wed': None,
                        'thr': None,
                    }

                    if dusers.exists():
                        duser = dusers[0]

                        for i, day in enumerate(content.keys()):
                            schedules = NightUserSchedule.objects.filter(
                                user=duser, date=date + timedelta(days=i))

                            if len(schedules) == 1:
                                schedule = schedules[0]

                            else:
                                for sc in schedules:
                                    sc.delete()
                                schedule = nightschedule_default_generator(
                                    user=duser, date=date + timedelta(days=i))

                            content[day] = schedule.jsonify()

                        content['message'] = ""

                    else:
                        duser = dormitoryuser_default_generator(user=user)

                        for i, day in enumerate(content.keys()):
                            schedule = nightschedule_default_generator(
                                user=duser, date=date + timedelta(days=i))

                            content[day] = schedule.jsonify()

                        content['message'] = "user information is deleted, plase rewrite the fixed_schedule"

                    result = True

                else:
                    content = "invalid auth"

            else:
                content = "invalid session"

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }), content_type='application/json')


@csrf_exempt
def get_all_nightschedule(request: HttpRequest):
    result, content = False, ""
    if request.method == "POST":
        flag = True
        try:
            recv = json.loads(request.body)
            session, date = \
                recv['session'], datetime.strptime(recv['date'], "%Y-%m-%d")
        except:
            content = "invalid data organization"
            flag = False

        if flag:
            res, login_session = multi_session(
                LoginSession.objects.filter(session=session)
            )

            if res:
                user = login_session.user

                if auth_binarify(user.auth)[6] == "1":
                    schedules = NightUserSchedule.objects.filter(date=date)
                    content = []

                    for sch in schedules:
                        if not sch.schedule == "1":
                            content.append(sch.jsonify())

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
    }), content_type="application/json")


@csrf_exempt
def set_student_participate(request: HttpRequest):
    result, content = False, ""
    if request.method == "POST":
        flag = True
        try:
            recv = json.loads(request.body)
            session, id = recv['session'], recv['id']
        except:
            content = "invalod data organization"
            flag = False

        if flag:
            res, login_session = multi_session(
                LoginSession.objects.filter(session=session)
            )

            if res:
                user = login_session.user

                if auth_binarify(user.auth)[6] == "1":
                    sch = NightUserSchedule.objects.filter(id=id)

                    if sch.exists():
                        sch[0].participate = not sch[0].participate
                        sch[0].save()
                        result = True

                    else:
                        content = "invalid id, reloading"

                else:
                    content = "invalid auth"

            else:
                content = login_session

    else:
        content = "invalid request method"

    return HttpResponse(json.dumps({
        "result": result,
        "content": content,
    }), content_type="application/json")
