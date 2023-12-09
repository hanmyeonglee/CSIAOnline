from django.db import models
from account.models import User


class DormitoryUser(models.Model):
    """
    기숙사 유저, AfterSchoolUser와 구분된다.\n
    Args:
        user -> User와 관계형, UNIQUE\n
        gender -> 성별(User에 저장할까 고민중)\n
        room -> 기숙사 방 호실 번호\n
        mon,tue,wed,thr_fixed -> fix된 nightschedule 리스트, ClassInformation의 숫자와 연결됨\n
        last_updated -> 업데이트할 시기를 알려줌
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=3)
    room = models.SmallIntegerField()
    mon_fixed = models.CharField(max_length=3)
    tue_fixed = models.CharField(max_length=3)
    wed_fixed = models.CharField(max_length=3)
    thr_fixed = models.CharField(max_length=3)
    last_updated = models.DateField()

    def jsonify(self):
        return {
            "user": self.user.name,
            "gender": self.gender,
            "room": self.room,
            "mon_fixed": self.mon_fixed,
            "tue_fixed": self.tue_fixed,
            "wed_fixed": self.wed_fixed,
            "thr_fixed": self.thr_fixed,
        }

    def simple_jsonify(self):
        return {
            "user": self.user.name,
            "gender": self.gender,
        }


class NightUserSchedule(models.Model):
    """
    Dormitory User의 NightSchedule을 date에 따라 저장한다.\n
    Args:
        user -> DormitoryUser, 관계형, 일대일이다.\n
        schedule -> ClassInformation의 id와 같은 값을 가진다. 다만 1개\n
        date -> 진행할 날짜이다.
    """
    user = models.ForeignKey(DormitoryUser, on_delete=models.CASCADE)
    schedule = models.CharField(max_length=3)
    date = models.DateField()
    participate = models.BooleanField(default=False)

    def jsonify(self):
        return {
            "user": self.user.simple_jsonify(),
            "schedule": self.schedule,
            "id": self.id,
        }
