import secrets
import string


def generate():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
