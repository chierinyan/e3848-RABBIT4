import serial

arduino = serial.Serial('/dev/ttyUSB-arduino', 115200)

def base_ctl(lx, ly, az, arm):

    cmd = bytes([255, lx, ly, az, arm])
    arduino.write(cmd)
    ultrasonic = arduino.read()
    try:
        ultrasonic = int.from_bytes(ultrasonic, byteorder='big')
    except ValueError:
        ultrasonic = -1
    return ultrasonic

if __name__ == '__main__':
    while True:
        ultrasonic = base_ctl(0,0,35,0)
        print(ultrasonic)
