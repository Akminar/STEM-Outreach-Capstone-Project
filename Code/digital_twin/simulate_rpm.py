import serial
import time
import random

SIMULATED_PORT = "/dev/ttys004"  # Replace with the first PTY from socat

ser = serial.Serial(SIMULATED_PORT, 115200, timeout=1)


while True:
    simulated_rpm = (3 + random.uniform(-2, 2)) * 60
    ser.write(f"{simulated_rpm}\n".encode())
    time.sleep(3)
