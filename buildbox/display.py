#!/usr/bin/python

from i2clibraries import i2c_lcd
from user import User
import time
import json
import math
import socket
import urllib.request
import traceback

# Configuration parameters
# I2C Address, Port, Enable pin, RW pin, RS pin, Data 4 pin, Data 5 pin, Data 6 pin, Data 7 pin, Backlight pin (optional)
lcd = i2c_lcd.i2c_lcd(0x27, 1, 2, 1, 0, 4, 5, 6, 7, 3)

# If you want to disable the cursor, uncomment the following line
lcd.command(lcd.CMD_Display_Control | lcd.OPT_Enable_Display)

lcd.backLightOn()

clearScreen = "                " # Clear the screen with empty string

def checkApiStatus():
    try:
        urllib.request.urlopen('https://build-box-test.herokuapp.com', timeout=5)
        return True
    except Exception:
        traceback.print_exc()
        return False


def chunkMsg(msg):
    avg = len(msg) / float(16)
    lines = math.ceil(avg)
    out = []

    for line in range(0, lines):
        if len(msg) - (line * 16) < 16:
            spacesNeeded = 16 - len(msg[(line * 16):])
            lastMsgWithSpaces = msg[(line * 16):]
            for i in range(0, spacesNeeded):
                lastMsgWithSpaces = lastMsgWithSpaces + " "
            out.append(lastMsgWithSpaces)
        else:
            out.append(msg[(line * 16):-(len(msg) - ((line * 16) + 16))])
    return out


def writeToScreen(msg):
    msgChunkArr = chunkMsg(msg)

    for line in range(0, len(msgChunkArr)):
        lcd.setPosition(1, 0)
        lcd.writeString(msgChunkArr[line])
        if line + 1 < len(msgChunkArr):
            lcd.setPosition(2, 0)
            lcd.writeString((msgChunkArr[line + 1]))
        else:
            lcd.setPosition(2, 0)
            lcd.writeString(clearScreen)
        time.sleep(1.5)

if checkApiStatus():
    users = []

    with open('userStats.json') as data_file:
        data = json.load(data_file)

    for user in range(0, len(data['users'])):
        users.append(User(data['users'][user]['id'], data['users'][user]['name'], data['users'][user]['attempts'],
                          data['users'][user]['succeeds'], data['users'][user]['fails']))

    while True:
        lcd.clear()
        if checkApiStatus():
            writeToScreen("This build box is so amazing, such wow! :ok: lol we need hot pockets")
            writeToScreen("Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mattis ante. Sed rutrum vehicula vestibulum. In maximus nisl non neque laoreet viverra. Nam auctor erat sed est pretium mollis. Aliquam lobortis diam ac urna convallis scelerisque. Donec dictum nisl nec metus imperdiet, eget condimentum velit maximus. Nullam ligula eros, dictum sit amet nisl sit amet, dignissim iaculis purus. Nullam tortor nisi, semper in molestie interdum, porta a lorem. Curabitur vestibulum sodales erat, vitae viverra lacus iaculis non.")
        else:
            lcd.writeString("Error connecting")

        time.sleep(5)
