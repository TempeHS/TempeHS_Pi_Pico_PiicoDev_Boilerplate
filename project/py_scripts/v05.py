"""
Sample simple servo smoothing, which reduces
jerk, vibration, and mechanical stress by softening
transitions between target positions.
"""

import utime
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

time_last_change = utime.ticks_ms()
change_servo = False
change_tick = 0
servo_value = 1500
new_servo_value = 2000
servo_smooth_time = 750


def smooth_change():
    global servo_value
    global new_servo_value
    global change_servo
    global change_state
    global change_tick
    global servo_smooth_time

    if change_tick == 0:
        if servo_value > new_servo_value:
            servo_value -= 1
            change_tick = 1
        elif servo_value < new_servo_value:
            servo_value += 1
            change_tick = 1
        elif servo_value == new_servo_value:
            change_state = False
    elif (
        change_tick == 1
        and utime.ticks_diff(utime.ticks_ms(), time_last_change) >= servo_smooth_time
    ):
        change_tick = 0
    print(f"Servo value is now: {servo_value}")  # debugging only then remove


while True:
    my_servo.set_duty(servo_value)
    if servo_value != new_servo_value:
        if not change_servo:
            time_last_change = utime.ticks_ms()
            change_servo = True
        smooth_change()
