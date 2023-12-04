from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from .models import User, LoginSession
import json


def login(request: HttpRequest):
    if request.method == 'POST':
        ct = request.content_type

        if 'application/json' in ct:
            recv = json.loads(request.body)
            print(recv)
            return HttpResponse({
                "operation": "login",
                "body": {
                    "result": True,
                    "content": "abcd",
                }
            })

    return HttpResponse({
        "operation": "login",
        "body": {
            "result": False,
            "content": "",
        }
    })
