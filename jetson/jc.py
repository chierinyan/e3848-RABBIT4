from time import sleep
from pyjoycon import JoyCon, get_R_id

class JC:
    cal_x = (2165, 1280)
    cal_y = (1845, 1115)
    deadzone = 0.45
    def __init__(self):
        joycon_id = get_R_id()
        self.joycon = JoyCon(*joycon_id)
        self.stick = {'x':0, 'y':0}
        self.buttons = {'x':0, 'y':0, 'a':0, 'b':0, 'r':0}
        self.pressed = {'x':0, 'y':0, 'a':0, 'b':0, 'r':0}
        sleep(0.5)

    def update_status(self):
        status = self.joycon.get_status()
        stick = status['analog-sticks']['right']
        buttons = status['buttons']['right']
        buttons['r'] = buttons['r'] | buttons['zr']

        self.stick['x'] = (stick['horizontal'] - JC.cal_x[0]) / JC.cal_x[1]
        if abs(self.stick['x']) < JC.deadzone: self.stick['x'] = 0
        self.stick['y'] = (stick['vertical'] - JC.cal_y[0]) / JC.cal_y[1]
        if abs(self.stick['y']) < JC.deadzone: self.stick['y'] = 0

        for button in self.buttons:
            self.pressed[button] = buttons[button] & (1 - self.buttons[button])
            self.buttons[button] = buttons[button]

if __name__ == '__main__':
    jc = JC()
    while True:
        jc.update_status()
        print(round(jc.stick['x'], 2), round(jc.stick['y'], 2))
        sleep(1)
