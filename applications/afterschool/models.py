from django.db import models


class SeatNumber(models.Model):
    """
    각 학번마다 야자실 자리 번호를 지정함\n
    여기 없는 학번은 교실 자습임\n
    Args:
        number -> 학번\n
        seat_number -> 자리 번호
    """
    number = models.CharField(max_length=10, primary_key=True)
    seat_number = models.SmallIntegerField()


class Supervisor(models.Model):
    """
    각 날짜마다 감독 교사 이름을 입력함\n
    Args:
        name -> 감독 교사 이름\n
        date -> 날짜
    """
    date = models.DateField(primary_key=True)
    name = models.CharField(max_length=64)


class ClassInformation(models.Model):
    """
    각 방과후/주문형마다 아이디(숫자), 수업 이름/장소를 저장함
    Args:
        id -> 수업 아이디(숫자)\n
        class_name -> 수업명\n
        class_location -> 수업 위치\n
        class_time -> 수업 시간, 000 ~ 111까지 binary로 나타냄(저장할 땐 숫자)
        teacher -> 수업 교사
    """
    id = models.SmallIntegerField(primary_key=True)
    class_name = models.CharField(max_length=255)
    class_location = models.CharField(max_length=255)
    class_time = models.SmallIntegerField()
    teacher = models.CharField(max_length=64)

    def jsonify(self):
        return {
            "id_number": self.id,
            "class_name": self.class_name,
            "class_location": self.class_location,
            "class_time": bin(self.class_time)[2:],
            "teacher": self.teacher,
        }


class UserWeekSchedule(models.Model):
    """
    각 user의 한 주 스케쥴을 012 등의 숫자 배열로 담는다.\n
    숫자는 ClassInformation의 아이디이다.\n
    Args:
        user -> 유저 정보\n
        mon, tue, wed, thr -> 유저가 이번주 신청한 스케쥴\n
        mon,tue,wed,thr_fixed -> 유저가 정한 fixed한 스케쥴\n
        date -> 오늘 날짜
    """
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    mon = models.CharField(max_length=5)
    tue = models.CharField(max_length=5)
    wed = models.CharField(max_length=5)
    thr = models.CharField(max_length=5)
    mon_fixed = models.CharField(max_length=5)
    tue_fixed = models.CharField(max_length=5)
    wed_fixed = models.CharField(max_length=5)
    thr_fixed = models.CharField(max_length=5)
    date = models.DateField()

    def __str__(self):
        return f"Week Schedule of ({self.user}) on {self.date.strftime('%Y/%m/%d')}"

    def jsonify(self):
        return {
            "date": self.date.strftime('%Y/%m/%d'),
            "mon": self.mon,
            "tue": self.tue,
            "wed": self.wed,
            "thr": self.thr,
        }
