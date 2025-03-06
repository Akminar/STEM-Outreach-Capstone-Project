import serial
import time
import random

ser = serial.Serial('/dev/ttyS0', 115200, timeout = 1)

while True:
    simulated_rpm = 30 + random.uniform(-5, 5)
    ser.write(f"{simulated_rpm}\n".encode())
    time.sleep(1)