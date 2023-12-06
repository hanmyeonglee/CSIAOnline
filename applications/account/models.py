from django.db import models
from datetime import datetime, timezone


class User(models.Model):
    """
    Instances:
        name -> 유저 이름\n
        grade -> 유저 학년\n
        classroom -> 유저 반\n
        number -> 유저 번호\n
        auth -> 유저 권한(현재 권한은 야자/기숙사 두 개)\n\t 00, 01, 10, 11로 나타냄(앞이 기숙사, 뒤가 야자)\n
        user_id -> 유저 아이디(중복 불가)\n
        password -> 패스워드
    Warnings:
        선생님들은 기본적으로 grade = classroom = number = 0이다.\n
        다만 name = "school", auth = 01과 name = "dorm", auth = 10인 쌤\n
        그리고 name = "master", auth = 11인 쌤이 존재한다.\n
        학생들은 기본적으로 auth = 00이다.
    """
    name = models.CharField(max_length=15)
    grade = models.SmallIntegerField()
    classroom = models.SmallIntegerField()
    number = models.SmallIntegerField()
    auth = models.SmallIntegerField()
    user_id = models.CharField(max_length=255, default="default_id")
    password = models.CharField(max_length=70)

    def __str__(self):
        return f"#{self.grade}-{self.classroom}-{str(self.number).ljust(2, '0')}-{bin(self.auth)[2:]}"

    def numbify(self):
        """
        학생의 정보를 학번으로 직렬화하여 출력한다.\n
        선생님들은 H00000과 같이 invalid하게 나온다.
        """
        return f"H{self.grade}0{self.classroom}{str(self.number).ljust(2, '0')}"

    def jsonify(self):
        """
        각 유저의 auth, name, number, id를 dict 형태로 출력한다.\n
        선생님의 경우 name, number, id는 거의 쓸모없다.
        """
        return {
            "auth": bin(self.auth)[2:],
            "name": self.name,
            "number": self.numbify(),
            "id": self.user_id,
        }


class LoginSession(models.Model):
    """
    Instances:
        student -> User Model(Table)에 Relative한 자료이다, 각 유저 로그인의 Session을 담당한다.\n
        session -> 세션이다. 항상 64bytes 길이를 가진다\n
        allot_time -> 로그인한 시점이다.\n
    Warnings:
        선생님들은 한 개의 계정만을 가진다.\n
        다만 로그인이 이미 있는 세션으로 이루어지는 경우를 제외하고는\n
        원래 있는 세션과 비교하여 그 세션을 바꾼다.\n
        즉, 모든 선생님 로그인마다 세션을 발급하며\n
        그 개수는 최대 선생님의 수만큼 나온다.
    Todo:
        id session 삭제/재발급 할 때마다 다시 1로 초기화하는거... 필요하나?
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.CharField(max_length=32)
    allot_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user} : session id={self.session}"

    def is_over(self):
        """
        이 세션이 1주가 지난 session인지 말한다.\n
        맞다면 True, 아니라면 False를 반환한다.
        """
        return True if (datetime.now(timezone.utc) - self.allot_time).seconds > 604800 else False

    def initialize_session(self, session):
        """
        Params:
            session -> 재발급한 session
        session을 재발급한다.\n
        동시에 time로 재발급한다.\n
        db에 저장하는 것에 성공하면 True, 실패하면 False를 반환함.
        """
        try:
            self.session = session
            self.allot_time = datetime.now(timezone.utc)
            self.save()
        except:
            return False
        return True
