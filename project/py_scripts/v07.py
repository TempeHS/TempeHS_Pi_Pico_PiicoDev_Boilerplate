"""
Example PID controller for cruise control using continuous servo and ultrasonic sensor

This example demonstrates a cruise control system that maintains a target distance
from an object using a continuous servo motor controlled by a PID controller.
"""

from PiicoDev_Ultrasonic import PiicoDev_Ultrasonic
from PiicoDev_Unified import sleep_ms
from machine import Pin, PWM
from servo import Servo
from PID_Controller import PIDControl

# System Configuration
TARGET_DISTANCE = 200  # Target distance in mm
SAMPLE_TIME = 100  # PID sample time in ms

# Create ultrasonic distance sensor object
range_sensor = PiicoDev_Ultrasonic(id=[0, 0, 0, 0])

# Create PWM servo controller (pin 16 on Pico)
servo_pwm = PWM(Pin(16))

# Continuous servo parameters (different from standard servo)
freq = 50
min_us = 500  # Full reverse
max_us = 2500  # Full forward
dead_zone_us = 1500  # Stop position

# Create continuous servo object
continuous_servo = Servo(
    pwm=servo_pwm, min_us=min_us, max_us=max_us, dead_zone_us=dead_zone_us, freq=freq
)

# Create PID controller for cruise control
# Output range: 1000-2000us (reverse to forward, with 1500us = stop)
pid = PIDControl(
    Kp=2.0,  # Proportional gain - how aggressively to respond to error
    Ki=0.05,  # Integral gain - eliminates steady-state error
    Kd=0.5,  # Derivative gain - reduces overshoot
    T=SAMPLE_TIME,  # Sample time in milliseconds
    max_control=500,  # Maximum control signal (+500 from center)
    min_control=-500,  # Minimum control signal (-500 from center)
)

# Set the target distance
pid.setpoint = TARGET_DISTANCE

print("=== PID Cruise Control System ===")
print(f"Target Distance: {TARGET_DISTANCE}mm")
print(f"PID Gains - Kp:{pid.Kp}, Ki:{pid.Ki}, Kd:{pid.Kd}")
print("Starting control loop...")
print("Distance(mm) | Error(mm) | Control | Servo(us)")
print("-" * 50)

while True:
    # Read current distance from sensor
    current_distance = range_sensor.distance_mm

    # Update PID controller with current measurement
    pid.sensed_output = current_distance

    # Calculate PID control output
    control_signal = pid.compute()

    # Convert control signal to servo microseconds
    # Center position (1500us) + control offset
    servo_microseconds = int(dead_zone_us + control_signal)

    # Apply servo control
    continuous_servo.set_duty(servo_microseconds)

    # Calculate error for display
    error = TARGET_DISTANCE - current_distance

    # Display status information
    print(
        f"{current_distance:8.1f} | {error:8.1f} | {control_signal:7.1f} | {servo_microseconds:8d}"
    )

    # Control loop timing
    sleep_ms(SAMPLE_TIME)
