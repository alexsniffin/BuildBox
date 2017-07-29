#!/usr/bin/python

from user import User
import time
import json
import math
import socket
import urllib.request
import traceback


def checkApiStatus():
    try:
        urllib.request.urlopen('http://build-box-test.herokuapp.com', timeout=5)
        return True
    except Exception:
        traceback.print_exc()
        return False


def chunkMsg(msg):
    avg = len(msg) / float(16)
    lines = math.ceil(avg)
    out = []

    for line in range(0, lines):
        if len(msg) - line * 16 - 16 < 16:
            out.append(msg[(line * 16):])
        else:
            out.append(msg[(line * 16):-(len(msg) - line * 16 - 16)])

    return out


if checkApiStatus():
    users = []

    with open('userStats.json') as data_file:
        data = json.load(data_file)

    for user in range(0, len(data['users'])):
        users.append(User(data['users'][user]['id'], data['users'][user]['name'], data['users'][user]['attempts'],
                          data['users'][user]['succeeds'], data['users'][user]['fails']))
        print (users[0].name)

print (chunkMsg('this is a long msg of characters'))
