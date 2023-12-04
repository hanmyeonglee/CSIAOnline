from .models import User
from random import randint
from hashlib import sha256


def main():
    names = [
        "Liam", "Olivia", "Noah", "Emma", "Oliver",
        "Charlotte", "James", "Amelia", "Elijah", "Sophia",
        "William", "Isabella", "Henry", "Ava", "Lucas",
        "Mia", "Benjamin", "Evelyn", "Theodore", "Luna",
    ]

    for name in names:
        tmp = User(name=name, grade=randint(1, 3), classroom=randint(1, 4), number=randint(
            1, 30), auth=0, user_id=name, password=sha256(sha256("1234".encode()).digest()).hexdigest())
        tmp.save()
