"""
Sample code for servo library, demonstrating instantiation
and setting angles for a positional servo. The resulting angles
of a set_angle(x) call are:

| Set angle | 180 Servo | 270 Servo |
| --------- | --------- | --------- |
|     0     |     0     |     0     |
|     90    |     90    |     135   |
|     180   |     180   |     270   |

"""

import time
from servo import Servo
from machine import Pin, PWM

servo_pwm = PWM(Pin(16))

# Set the parameters of the servo pulses, more details in the "Documentation" section
freq = 50
min_us = 500
max_us = 2500
dead_zone_us = 1500

# create a servo object
my_servo = Servo(
    pwm=servo_pwm, min_us=min_us, max_us=max_us, dead_zone_us=dead_zone_us, freq=freq
)


while True:
    # Set the Servo to the mid-point (90 is half way between zero and 180 degrees)
    my_servo.set_angle(0)
    time.sleep(5)  # Wait for 1 second
    print("Servo at 0 degrees")

    # Set the Servo to the left most position
    my_servo.set_angle(90)
    time.sleep(2)  # Wait for 1 second
    print("Servo Stop")

    # Set the Servo to the right most position
    my_servo.set_angle(180)
    time.sleep(5)  # Wait for 1 second
    print("Servo at 180 degrees")

    # Set the Servo to the left most position
    my_servo.set_angle(90)
    time.sleep(2)  # Wait for 1 second
    print("Servo Stop")
