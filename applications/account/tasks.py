from background_task import background
from account.models import User
from afterschool.models import AfterSchoolUser, UserWeekSchedule, ClassInformation
from datetime import datetime
from pytz import timezone
import gspread

days = ['월', '화', '수', '목', '금', '토', '일']


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

# @background(schedule = 86400)


def scheduled_task():
    info = {}
    for cls in ClassInformation.objects.all():
        tmp = cls.jsonify()
        num = tmp['id_number']
        del tmp['id_number']
        info[num] = tmp

    sa = gspread.service_account(
        r"./gspread/service_account.json")

    sh = sa.open("testSheet")
    n = now()

    wks_r = sh.worksheet(f"({days[n.weekday()]})열람실")
    wks_c = sh.worksheet(f"({days[n.weekday()]})교실")

    for col_jump in range(2, 52, 11):
        for col in [col_jump, col_jump+5]:
            for row in range(1, 80):
                cell = wks_r.cell(row=row, col=col)

                try:
                    if not cell.value:
                        raise Exception()
                    snumber = cell.value

                    user = User.objects.get(user_id=snumber)
                    auser = AfterSchoolUser.objects.get(user=user)
                    schedule = UserWeekSchedule.objects.get(user=auser)

                    schs = list(map(int, schedule.schedule.split("/")))

                    first = info[schs[0]]['class_type']
                    second = info[schs[1]]['class_type']
                    third = info[schs[2]]['class_type']
                except:
                    first = "야자"
                    second = "야자"
                    third = "야자"

                wks_r.cell(row=row-1, col=col+3).value = first
                wks_r.cell(row=row, col=col+3).value = second
                wks_r.cell(row=row+1, col=col+3).value = third

    for col in [1, 8]:
        for row in range(4, 64):
            cell = wks_c.cell(row=row, col=col)
            try:
                if not cell.value:
                    raise Exception()
                snumber = cell.value

                user = User.objects.get(user_id=snumber)
                auser = AfterSchoolUser.objects.get(user=user)
                schedule = UserWeekSchedule.objects.get(user=auser)

                schs = list(map(int, schedule.schedule.split("/")))

                first = info[schs[0]]['class_type']
                second = info[schs[1]]['class_type']
                third = info[schs[2]]['class_type']
            except:
                first = "야자"
                second = "야자"
                third = "야자"

            wks_c.cell(row=row, col=col+2).value = first
            wks_c.cell(row=row, col=col+3).value = second
            wks_c.cell(row=row, col=col+4).value = third
