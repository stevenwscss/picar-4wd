import picar_4wd as fc
import sys
import tty
import termios
import asyncio
import time
from picar_4wd.speed import Speed

power_val = 50
key = 'status'
print("If you want to quit.Please press q")
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

def Keyborad_control():
    while True:
        global power_val
        key=readkey()
        if key=='6':
            if power_val <=90:
                power_val += 10
                print("power_val:",power_val)
        elif key=='4':
            if power_val >=10:
                power_val -= 10
                print("power_val:",power_val)
        if key=='w':
            fc.forward(power_val)
        elif key=='a':
            fc.turn_left(power_val)
        elif key=='s':
            fc.backward(power_val)
        elif key=='d':
            fc.turn_right(power_val)
        else:
            fc.stop()
        if key=='q':
            print("quit")  
            break

def move25():
    speed4 = Speed(25)
    speed4.start()
    # time.sleep(2)
    fc.backward(100)
    x = 0
    for i in range(1):
        time.sleep(0.1)
        speed = speed4()
        x += speed * 0.1
        print("%smm/s"%speed)
    print("%smm"%x)
    speed4.deinit()

    # time.sleep(0.1)

    fc.stop()












def scan_step(ref):
    scan_list = []
    current_angle = 0
    STEP = 18
    us_step = STEP
    current_angle += us_step
    angle_distance = [0,0]
    current_angle = 0
    ANGLE_RANGE = 180
    max_angle = ANGLE_RANGE/2
    min_angle = -ANGLE_RANGE/2
    
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP #-18, sweep backward
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    status = get_status_at(current_angle, ref1=ref) #ref1

    scan_list.append(status)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            # print("reverse")
            scan_list.reverse()
        # print(scan_list)
        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return False


# This function tests the ultrasonic sensor and the servo
def test_ultrasonic():
    # default 18 step
    # current_angle = 0
    # angle_range = 180
    # us_step = STEP = 18
    # scan_list = []
    while True:
        scanList = fc.scan_step(35)
        print(scanList)
        if not scanList:
            continue
        print("let's go forward")


if __name__ == '__main__':
    test_ultrasonic()






