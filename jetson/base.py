import serial

ser = serial.Serial('/dev/arduino')


def base_ctl(x, y, z, arm):
    vel = [f'{x}\n'.encode(),
           f'{y}\n'.encode(),
           f'{z}\n'.encode(),
           f'{arm}\n'.encode(),
           b'-1\n']
    ser.writelines(vel)

if __name__ == '__main__':
    from time import sleep
    while True:
        base_ctl(0, 0, 35, 1)
        ultrasonic = int(ser.readline().decode())
        print(ultrasonic)
        sleep(1)
