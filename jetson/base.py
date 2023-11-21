import serial
from time import sleep

class Base:
    def __init__(self):
        self.connect()

    def connect(self):
        while True:
            try:
                self.arduino = serial.Serial('/dev/ttyUSB-arduino', 115200)
                break
            except Exception as e:
                print(e)
                sleep(0.1)

    def base_ctl(self, lx, ly, az, arm):
        try:
            cmd = [255]
            for i in lx, ly, az:
                x = i + 100
                if x < 0: x = 0
                elif x > 200: x = 200
                cmd.append(x)
            cmd.append(arm)
            cmd = bytes(cmd)
            self.arduino.write(cmd)
            ultrasonic = self.arduino.read()
            ultrasonic = int.from_bytes(ultrasonic, byteorder='big')
            return ultrasonic
        except Exception as e:
            print(e)
            self.connect()
            return -1

if __name__ == '__main__':
    base = Base()

    arm = 1
    while True:
        arm = 1-arm
        ultrasonic = base.base_ctl(0,0,0,arm)
        print(ultrasonic)
        sleep(1)
