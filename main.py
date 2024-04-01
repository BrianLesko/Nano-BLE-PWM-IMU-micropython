# Brian Lesko 
# 3/25/2024
# Nano BLE Sense R2 

import time
import imu
from machine import Pin, I2C
from board import LED
led_red = LED(1)
led_green = LED(2)
led_blue = LED(3)

# PWM
from machine import Pin, PWM, ADC
a2 = Pin(27)
# pin 21 is Pin D8      # pin 23 is Pin D7      # Pin 24 is D3      # Pin 27 is D9
pwm = PWM(a2)
duty = 30000 # sets the duty cycle
pwm.freq(50) # standard is 50 Hz for Servos

# Serial communication
from machine import UART
BAUD = 115200
uart = UART(0, BAUD)

# IMU
bus = I2C(1, scl=Pin(15), sda=Pin(14))
imu = imu.IMU(bus)

def set_servo_angle(angle):
    # Convert the angle to pulse width
    pulse_width = (angle / 180) * 1000 + 1000  # Scale from 1ms to 2ms
    duty = int((pulse_width / 20000) * 65535)  # Convert to duty cycle (0-65535 range)
    pwm.duty_u16(duty)
    
def check_uart():
    while uart.any():
        data = uart.readline()  # Read a line of data from the UART
        data_str = data.decode().strip()  # Decode byte data to string
        print(data.decode())  # Decode byte data to string and print it
        
        if data_str == 'IMU':
            print('Accelerometer: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*imu.accel()))
            print('Gyroscope:     x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*imu.gyro()))
            print('Magnetometer:  x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*imu.magnet()))
            print("")
        
        try:
            data_float = float(data_str)  # Try to convert the data to a float
            #set_servo_angle(data_float*180)
            print(f"Set the servo angle to {data_float*180}")
            print("")
        except ValueError:
            print("there was an error")
            pass  # If data is not a number, do nothing

while (True):
   
    # Turn on LEDs
    led_red.on()
    led_green.on()
    led_blue.on()
    
    check_uart()
    time.sleep(0.1)     
            
    # Turn off LEDs
    led_red.off()
    led_green.off()
    led_blue.off()
    
    time.sleep(0.1)  # Sleep for 100ms
        
        
    