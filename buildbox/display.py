#!/usr/bin/python

from i2clibraries import i2c_lcd
from user import User
import time
import json
import socket
import urllib.request
import traceback

# Configuration parameters
# I2C Address, Port, Enable pin, RW pin, RS pin, Data 4 pin, Data 5 pin, Data 6 pin, Data 7 pin, Backlight pin (optional)
lcd = i2c_lcd.i2c_lcd(0x27, 1, 2, 1, 0, 4, 5, 6, 7, 3)

# If you want to disable the cursor, uncomment the following line
lcd.command(lcd.CMD_Display_Control | lcd.OPT_Enable_Display)

lcd.backLightOn()

def checkApiStatus():
	try:
		urllib.request.urlopen('http://wwww.build-box.test.herokuapp.com', timeout=5)
		return True
	except Exception:
		traceback.print_exc()
		return False

if checkApiStatus():
	users = []

	with open('data.json') as data_file:
		data = json.load(data_file)

	for user in len(data['users']):
		users.append(User(data['users']['id'], data['users']['name']), data['users']['attempts'], data['users']['succeeds'], data['users']['fails'])
		print users[0].name

	while True:
		lcd.clear()
		if checkApiStatus():
			lcd.writeString([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
			lcd.setPosition(2, 0)
			lcd.writeString("Connected as    ")
			time.sleep(2.5)
			lcd.setPosition(2, 0)
			lcd.writeString("Status: Good    ")
		else:
			lcd.writeString("Error connecting")

		time.sleep(5)
