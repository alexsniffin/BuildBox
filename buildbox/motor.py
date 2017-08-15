import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
enable_pin = 18
coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 23
coil_B_2_pin = 24
 
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
 
GPIO.output(enable_pin, 1)

pass_next_state_steps = 160
build_next_state_steps = 170
fail_next_state_steps = 180

pass_next_state = 'BUILD'
build_next_state = 'FAIL'
fail_next_state = 'PASS'

current_state = 'FAIL'

delay = 2


def next_state():
    global current_state, delay
    if current_state == 'FAIL':
        forward(delay, fail_next_state_steps)
        current_state = fail_next_state
    elif current_state == 'PASS':
        forward(delay, pass_next_state_steps)
        current_state = pass_next_state
    elif current_state == 'BULD':
        forward(delay, build_next_state_steps)
        current_state = build_next_state


def forward(delay, steps):
    for i in range(0, steps):
        set_step(1, 0, 1, 0)
        time.sleep(delay)
        set_step(0, 1, 1, 0)
        time.sleep(delay)
        set_step(0, 1, 0, 1)
        time.sleep(delay)
        set_step(1, 0, 0, 1)
        time.sleep(delay)
 
#def backwards(delay, steps):
#  for i in range(0, steps):
#    set_step(1, 0, 0, 1)
#    time.sleep(delay)
#    set_step(0, 1, 0, 1)
#    time.sleep(delay)
#    set_step(0, 1, 1, 0)
#    time.sleep(delay)
#    set_step(1, 0, 1, 0)
#    time.sleep(delay)
 
  
def set_step(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)
 
while True:
    state_wanted = raw_input("What state do you want? ")
    while current_state != state_wanted.upper():
        next_state()
