# Brian Lesko 
# 3/25/2024
# Nano BLE Sense R2 

import time
import imu
from machine import Pin, I2C

from machine import Pin, PWM, ADC
a2 = Pin(27)
# pin 21 is Pin D8      # pin 23 is Pin D7      # Pin 24 is D3      # Pin 27 is D9
pwm = PWM(a2)
duty = 30000 # sets the duty cycle
pwm.freq(50) # standard is 50 Hz for Servos

bus = I2C(1, scl=Pin(15), sda=Pin(14))
imu = imu.IMU(bus)

def set_servo_angle(angle):
    # Convert the angle to pulse width
    pulse_width = (angle / 180) * 1000 + 1000  # Scale from 1ms to 2ms
    duty = int((pulse_width / 20000) * 65535)  # Convert to duty cycle (0-65535 range)
    pwm.duty_u16(duty)

while (True):
    print('Accelerometer: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*imu.accel()))
    print('Gyroscope:     x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*imu.gyro()))
    print('Magnetometer:  x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*imu.magnet()))
    print("")
    time.sleep_ms(100)
    
    set_servo_angle(0)  # Minimum angle
    time.sleep_ms(300)
    set_servo_angle(180)  # Maximum angle
    time.sleep_ms(300)
    #PWM(Pin(n), freq=1_000_000, period=1000)