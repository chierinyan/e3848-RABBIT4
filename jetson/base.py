import serial
from time import sleep

arduino = serial.Serial('/dev/ttyUSB-arduino', 115200)

def base_ctl(lx, ly, az, arm):
    cmd = [255]
    for i in lx, ly, az:
        x = i + 100
        if x < 0: x = 0
        elif x > 200: x = 200
        cmd.append(x)
    cmd.append(arm)
    cmd = bytes(cmd)
    arduino.write(cmd)
    ultrasonic = arduino.read()
    ultrasonic = int.from_bytes(ultrasonic, byteorder='big')
    return ultrasonic

if __name__ == '__main__':
    arm = 1
    while True:
        arm = 1-arm
        ultrasonic = base_ctl(0,0,0,arm)
        print(ultrasonic)
        sleep(1)
