"""
Sample code for a simple state machine
"""

from machine import Pin, PWM
from servo import Servo
from machine import RTC


# create a PWM servo controller (16 - pin Pico)
servo_pwm = PWM(Pin(16))
rtc = RTC()

# Set the parameters of the servo pulses, more details in the "Documentation" section
freq = 50
min_us = 500
max_us = 2500
dead_zone_us = 1500

# create a servo object
my_servo = Servo(
    pwm=servo_pwm, min_us=min_us, max_us=max_us, dead_zone_us=dead_zone_us, freq=freq
)

time_last_change = rtc.datetime()
machine_state = 1
state_1_time = 3
state_1_state = 500
state_2_time = 6
state_2_state = 1000
state_3_time = 9
state_3_state = 1500
state_4_time = 12
state_4_state = 2000


while True:
    time_now = rtc.datetime()

    if machine_state == 1:
        my_servo.set_duty(state_1_state)
        if time_now[6] - time_last_change[6] >= state_1_time:
            machine_state = 2
    elif machine_state == 2:
        my_servo.set_duty(state_2_state)
        if time_now[6] - time_last_change[6] >= state_2_time:
            machine_state = 3
    elif machine_state == 3:
        my_servo.set_duty(state_3_state)
        if time_now[6] - time_last_change[6] >= state_3_time:
            machine_state = 4
    elif machine_state == 4:
        my_servo.set_duty(state_4_state)
        if time_now[6] - time_last_change[6] >= state_4_time:
            time_last_change = rtc.datetime()
            machine_state = 1
