from jc import JC
from time import sleep
from base import Base

if __name__ == '__main__':
    jc = JC()
    base = Base()

    arm = 1
    while True:
        jc.update_status()

        if jc.buttons['r']:
            lx = 0; ly = 0; az =0
        else:
            lx = round(jc.stick['y'] * 45)
            if abs(lx) < 10: lx = 0
            az = round(jc.stick['x'] * -45)
            if abs(az) < 10: az = 0

            ly = 0
            if jc.buttons['a']: ly = 35
            elif jc.buttons['y']: ly = -35

        if jc.buttons['x']: arm = 0
        if jc.buttons['b']: arm = 1

        ut = base.base_ctl(lx, ly, az, arm)
        print(ut)

        sleep(0.1)
