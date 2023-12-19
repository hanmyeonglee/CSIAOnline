from django.db import models
from account.models import User


class SeatNumber(models.Model):
    """
    각 학번마다 야자실 자리 번호를 지정함\n
    여기 없는 학번은 교실 자습임\n
    Args:
        number -> 학번\n
        seat_number -> 자리 번호
    """
    number = models.CharField(max_length=16, primary_key=True)
    seat_number = models.SmallIntegerField(unique=True)


class Supervisor(models.Model):
    """
    각 날짜마다 감독 교사 이름을 입력함\n
    Args:
        name -> 감독 교사 이름\n
        date -> 날짜
    """
    date = models.DateField(primary_key=True)
    name = models.CharField(max_length=64)

    def jsonify(self):
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "name": self.name,
        }


class ClassInformation(models.Model):
    """
    각 방과후/주문형마다 아이디(숫자), 수업 이름/장소를 저장함(CSMP 포함)
    Args:
        id -> 수업 아이디(숫자)\n
        class_name -> 수업명\n
        class_location -> 수업 위치\n
        class_time -> 수업 시간, 000 ~ 111까지 binary로 나타냄(저장할 땐 숫자)\n
        teacher -> 수업 교사
    """
    class_name = models.CharField(max_length=255)
    class_location = models.CharField(max_length=255)
    class_time = models.CharField(max_length=64)
    class_type = models.CharField(max_length=64)
    teacher = models.CharField(max_length=64)

    def jsonify(self):
        return {
            "id_number": self.id,
            "class_name": self.class_name,
            "class_location": self.class_location,
            "class_time": self.class_time,
            "teacher": self.teacher,
            "class_type": self.class_type,
        }


class AfterSchoolUser(models.Model):
    """
    AfterSchool에서 사용하는 User 정보\n
    Args:\n
        user -> user 정보\n
        mon,tue,wed,thr_fixed -> 유저가 정한 fixed한 스케쥴\n
    Todo:
        마지막 업데이트 날짜 지정해서 학기/년도마다 업데이트 메시지 날려주기
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mon_fixed = models.CharField(max_length=16)
    tue_fixed = models.CharField(max_length=16)
    wed_fixed = models.CharField(max_length=16)
    thr_fixed = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.mon_fixed}|{self.tue_fixed}|{self.wed_fixed}|{self.thr_fixed} : {self.user}"

    def jsonify(self):
        return {
            "mon_fixed": self.mon_fixed,
            "tue_fixed": self.tue_fixed,
            "wed_fixed": self.wed_fixed,
            "thr_fixed": self.thr_fixed,
        }


class UserWeekSchedule(models.Model):
    """
    각 afterschool user의 한 주 스케쥴을 012 등의 숫자 배열로 담는다.\n
    숫자는 ClassInformation의 아이디이다.\n
    Args:
        user -> afterschool 유저 정보\n
        schedule -> 유저가 이번주 신청한 스케쥴\n
        date -> 오늘 날짜\n
        participate -> 야자 제대로 참가했는지\n
    Todo:\n
        아니 잠만 이거 date 정보가 있는데 왜 mon/tue/wed/thr을 담아놨지?
        이거 없애고 schedule 정보만 받는 걸로 수정하자.
    """
    user = models.ForeignKey(
        AfterSchoolUser, on_delete=models.CASCADE)
    schedule = models.CharField(max_length=16)
    date = models.DateField()
    participate = models.BooleanField(default=False)

    def __str__(self):
        return f"Week Schedule of ({self.user}) on {self.date.strftime('%Y-%m-%d')}"

    def jsonify(self):
        return {
            "schedule": self.schedule,
            "id": self.id,
        }


class SeminarRoomBook(models.Model):
    """
    room1~6_1~3 : 세미나실 룸 예약한 User id를 /로 구분해서 저장한다.\n
    date : 세머니실 예약 날짜\n
    예를 들어 유저 아이디 1, 2, 3이 room1을 1교시에 사용하고, 선생님께 수락되었다면,\n
    1/2/3=1, 수락 안됐으면 1/2/3=0으로 처리된다.\n
    Todo:\n
        세미나실 예약 기능 추가
    """
    room1_1 = models.CharField(max_length=64, default="")
    room1_2 = models.CharField(max_length=64, default="")
    room1_3 = models.CharField(max_length=64, default="")
    room2_1 = models.CharField(max_length=64, default="")
    room2_2 = models.CharField(max_length=64, default="")
    room2_3 = models.CharField(max_length=64, default="")
    room3_1 = models.CharField(max_length=64, default="")
    room3_2 = models.CharField(max_length=64, default="")
    room3_3 = models.CharField(max_length=64, default="")
    room4_1 = models.CharField(max_length=64, default="")
    room4_2 = models.CharField(max_length=64, default="")
    room4_3 = models.CharField(max_length=64, default="")
    room5_1 = models.CharField(max_length=64, default="")
    room5_2 = models.CharField(max_length=64, default="")
    room5_3 = models.CharField(max_length=64, default="")
    room6_1 = models.CharField(max_length=64, default="")
    room6_2 = models.CharField(max_length=64, default="")
    room6_3 = models.CharField(max_length=64, default="")
    date = models.DateField(unique=True)

    def simple_jsonify(self):
        return {
            "room1_1": bool(self.room1_1),
            "room1_2": bool(self.room1_2),
            "room1_3": bool(self.room1_3),
            "room2_1": bool(self.room2_1),
            "room2_2": bool(self.room2_2),
            "room2_3": bool(self.room2_3),
            "room3_1": bool(self.room3_1),
            "room3_2": bool(self.room3_2),
            "room3_3": bool(self.room3_3),
            "room4_1": bool(self.room4_1),
            "room4_2": bool(self.room4_2),
            "room4_3": bool(self.room4_3),
            "room5_1": bool(self.room5_1),
            "room5_2": bool(self.room5_2),
            "room5_3": bool(self.room5_3),
            "room6_1": bool(self.room6_1),
            "room6_2": bool(self.room6_2),
            "room6_3": bool(self.room6_3),
            "date": self.date.strftime("%Y-%m-%d"),
        }

    def jsonify(self):
        return {
            "room1_1": self.room1_1,
            "room1_2": self.room1_2,
            "room1_3": self.room1_3,
            "room2_1": self.room2_1,
            "room2_2": self.room2_2,
            "room2_3": self.room2_3,
            "room3_1": self.room3_1,
            "room3_2": self.room3_2,
            "room3_3": self.room3_3,
            "room4_1": self.room4_1,
            "room4_2": self.room4_2,
            "room4_3": self.room4_3,
            "room5_1": self.room5_1,
            "room5_2": self.room5_2,
            "room5_3": self.room5_3,
            "room6_1": self.room6_1,
            "room6_2": self.room6_2,
            "room6_3": self.room6_3,
            "date": self.date.strftime("%Y-%m-%d"),
        }
