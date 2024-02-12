import RPi.GPIO as gpio
from RpiMotorLib import RpiMotorLib
import time
import cv2 
import requests
import json
import yadisk
import datetime

with open('button.txt', 'w') as file:
    file.write('0')
url='https://api.ultralytics.com/v1/predict/NfS6VHgafxCkHkZ3a1ba'
headers={'x-api-key':'00f8da88e7a19b7a35b46b2f1e7d8c80585d03c37e'}
data={'size':640, 'confidence':0.25, 'iou':0.45}
width=18000
len_of_conveyer=690#+-20
dir1 = 19
step1 = 13
dir2=3
step2=2
dir3=20
step3=26
test1_challenge1=18
test1_challenge2=23
test1_challenge3=24
test3_full=8
stamp_print=15
on_off=14
test2=25
led_on_off=7
led_print_stamp=12
led_paper=6
foto=4
peeeep=17
mode=4
stamp=True
k=0

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(test1_challenge1, gpio.IN)
gpio.setup(foto, gpio.IN)
gpio.setup(test1_challenge2, gpio.IN)
gpio.setup(test1_challenge3, gpio.IN)
gpio.setup(test3_full, gpio.IN)
gpio.setup(stamp_print, gpio.IN)
gpio.setup(on_off, gpio.IN)
gpio.setup(test2, gpio.IN)
gpio.setup(on_off, gpio.IN)
gpio.setup(led_on_off, gpio.OUT)
gpio.setup(led_print_stamp, gpio.OUT)
gpio.setup(led_paper, gpio.OUT)
gpio.setup(peeeep, gpio.OUT)
    
        
ItsMyMotor1 = RpiMotorLib.A4988Nema(dir1, step1, (21, 21, 21), "A4988")
ItsMyMotor2 = RpiMotorLib.A4988Nema(dir2, step2, (21, 21, 21), "DRV8825")
ItsMyMotor3 = RpiMotorLib.A4988Nema(dir3, step3, (21, 21, 21), "A4988")

def test_1_1():
    print('*')
    ItsMyMotor2.motor_go(False, "Full", len_of_conveyer, 0.002, False, 0.05)
    time.sleep(5)
    ItsMyMotor2.motor_go(True, "Full", len_of_conveyer-200, 0.002, False, 0.05)
    time.sleep(5)
    ItsMyMotor2.motor_go(False, "Full", len_of_conveyer-200, 0.002, False, 0.05)
    time.sleep(5)
    ItsMyMotor2.motor_go(False, "Full", 1000, 0.002, False, 0.05)
def test_1_2():
    print('/')
    width=18000
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if ret:
            cv2.imwrite('/home/pi/ChepuhNYA/Test_image_1.png', frame)
            with open('/home/pi/ChepuhNYA/Test_image_1.png', 'rb') as f:
                res=requests.post(url, headers=headers, data=data, files={'image':f})
            cam.release()
            res.raise_for_status()
            dump=json.dumps(res.json(), indent=2)
            mas_of_dump=dump[18:dump.index(']')-3].split('}')
            del mas_of_dump[-1]
            for i in range(len(mas_of_dump)):
                mas_of_dump[i]=mas_of_dump[i][8:].split(',\n      ')
                for o in range(len(mas_of_dump[i])):
                    mas_of_dump[i][o]=tuple(mas_of_dump[i][o].split(': '))
                mas_of_dump[i]=dict(mas_of_dump[i])
            if len(mas_of_dump)==2:
                if float(mas_of_dump[0]['"confidence"']) > float(mas_of_dump[1]['"confidence"']):
                    mas_of_dump=mas_of_dump[0]
                    mas_of_dump['"ycenter"']=mas_of_dump['"ycenter"'][:-5]
                else:
                    mas_of_dump=mas_of_dump[1]
                    mas_of_dump['"ycenter"']=mas_of_dump['"ycenter"'][:-5]
            elif len(mas_of_dump)==0:
                    mas_of_dump={'"name"':'0', '"xcenter"':'1', '"ycenter"':'1'}
            else:
                mas_of_dump=mas_of_dump[0]
                mas_of_dump['"ycenter"']=mas_of_dump['"ycenter"'][:-5]
            important_information={'name':mas_of_dump['"name"'], 'xcenter':float(mas_of_dump['"xcenter"']), 'ycenter':float(mas_of_dump['"ycenter"'])}
            print(important_information)
            break
    if important_information['xcenter']<0.5:
        ItsMyMotor2.motor_go(True, "Full", round((len_of_conveyer+250)*important_information['xcenter']), 0.002, False, 0.05)
        time.sleep(1)
        width-=2000 if important_information['ycenter']<0.5 else +4000
        ItsMyMotor1.motor_go(False, "Full",round(width*(important_information['ycenter'])), 0.001, False, 0.05)
    else:
        ItsMyMotor2.motor_go(True, "Full", round((len_of_conveyer+100)*important_information['xcenter']), 0.002, False, 0.05)
        time.sleep(1)
        width-=2000 if important_information['ycenter']<0.5 else +4000
        ItsMyMotor1.motor_go(False, "Full",round(width*(important_information['ycenter'])), 0.001, False, 0.05)
    time.sleep(1)
    ItsMyMotor3.motor_go(True, "Full",4600, 0.0005, False, 0.05)
    time.sleep(1)
    ItsMyMotor3.motor_go(False, "Full", 4600, 0.0005, False, 0.05)
    ItsMyMotor1.motor_go(True, "Full",round(width*(important_information['ycenter'])), 0.001, False, 0.05)
def test_1_3():
    cam = cv2.VideoCapture(0)
    print('+')
    global k
    ret, frame = cam.read()
    if ret:
        k+=1
        cv2.imwrite('/home/pi/ChepuhNYA/Test_image_1.png', frame)
    a=time.localtime()
    y = yadisk.YaDisk(token='y0_AgAAAABxr3AqAAs6AQAAAAD5ul_iAADfMLvdY6VA27dwT4mN1eD3Xp6ksg')
    y.upload('/home/pi/ChepuhNYA/Test_image_1.png', f'/Project/{k}_{a[0]}_{a[1]}_{a[2]}_{a[3] if len(str(a[3]))==2 else "0"+str(a[3])}_{a[4] if len(str(a[4]))==2 else "0"+str(a[4])}_{a[5] if len(str(a[5]))==2 else "0"+str(a[5])}.pdf')
def test_2(stamp):
    global k
    width=18000
    print('-')
    cam = cv2.VideoCapture(0)
    ItsMyMotor2.motor_go(False, "Full", len_of_conveyer, 0.002, False, 0.05)
    while True:
        ret, frame = cam.read()
        if ret:
            cv2.imwrite('/home/pi/ChepuhNYA/Test_image_1.png', frame)
            with open('/home/pi/ChepuhNYA/Test_image_1.png', 'rb') as f:
                res=requests.post(url, headers=headers, data=data, files={'image':f})
            cam.release()
            res.raise_for_status()
            dump=json.dumps(res.json(), indent=2)
            mas_of_dump=dump[18:dump.index(']')-3].split('}')
            del mas_of_dump[-1]
            for i in range(len(mas_of_dump)):
                mas_of_dump[i]=mas_of_dump[i][8:].split(',\n      ')
                for o in range(len(mas_of_dump[i])):
                    mas_of_dump[i][o]=tuple(mas_of_dump[i][o].split(': '))
                mas_of_dump[i]=dict(mas_of_dump[i])
            if len(mas_of_dump)==2:
                if float(mas_of_dump[0]['"confidence"']) > float(mas_of_dump[1]['"confidence"']):
                    mas_of_dump=mas_of_dump[0]
                    mas_of_dump['"ycenter"']=mas_of_dump['"ycenter"'][:-5]
                else:
                    mas_of_dump=mas_of_dump[1]
                    mas_of_dump['"ycenter"']=mas_of_dump['"ycenter"'][:-5]
            elif len(mas_of_dump)==0:
                    mas_of_dump={'"name"':'0', '"xcenter"':'1', '"ycenter"':'1'}
            else:
                mas_of_dump=mas_of_dump[0]
                mas_of_dump['"ycenter"']=mas_of_dump['"ycenter"'][:-5]
            important_information={'name':mas_of_dump['"name"'], 'xcenter':float(mas_of_dump['"xcenter"']), 'ycenter':float(mas_of_dump['"ycenter"'])}
            print(important_information)
            break
    if (stamp and important_information['name'] == '"M._Sh"') or (not(stamp) and important_information['name'] == '"M._P."'):
        if important_information['xcenter']<0.5:
            ItsMyMotor2.motor_go(True, "Full", round((len_of_conveyer+250)*important_information['xcenter']), 0.002, False, 0.05)
            time.sleep(1)
            width-=2000 if important_information['ycenter']<0.5 else +4000
            ItsMyMotor1.motor_go(False, "Full",round(width*(important_information['ycenter'])), 0.001, False, 0.05)
        else:
            ItsMyMotor2.motor_go(True, "Full", round((len_of_conveyer+100)*important_information['xcenter']), 0.002, False, 0.05)
            time.sleep(1)
            width-=2000 if important_information['ycenter']<0.5 else +4000
            ItsMyMotor1.motor_go(False, "Full",round(width*(important_information['ycenter'])), 0.001, False, 0.05)    
        time.sleep(1)
        ItsMyMotor3.motor_go(True, "Full",4600, 0.0005, False, 0.05)
        time.sleep(1)
        ItsMyMotor3.motor_go(False, "Full", 4600, 0.0005, False, 0.05)
        time.sleep(1)
        if important_information['xcenter']<0.5:
            ItsMyMotor2.motor_go(False, "Full", round((len_of_conveyer+250)*important_information['xcenter']), 0.002, False, 0.05)
            time.sleep(1)
        else:
            ItsMyMotor2.motor_go(False, "Full", round((len_of_conveyer+100)*important_information['xcenter']), 0.002, False, 0.05)
            time.sleep(1)
        ItsMyMotor1.motor_go(True, "Full",round(width*(important_information['ycenter'])), 0.001, False, 0.05)
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if ret:
            k+=1
            cv2.imwrite('/home/pi/ChepuhNYA/Test_image_1.png', frame)
            break
    cam.release()
    a=time.localtime()
    y = yadisk.YaDisk(token='y0_AgAAAABxr3AqAAs6AQAAAAD5ul_iAADfMLvdY6VA27dwT4mN1eD3Xp6ksg')
    y.upload('/home/pi/ChepuhNYA/Test_image_1.png', f'/Project/{k}_{a[0]}_{a[1]}_{a[2]}_{a[3] if len(str(a[3]))==2 else "0"+str(a[3])}_{a[4] if len(str(a[4]))==2 else "0"+str(a[4])}_{a[5] if len(str(a[5]))==2 else "0"+str(a[5])}.pdf')
    ItsMyMotor2.motor_go(False, "Full", 1000, 0.002, False, 0.05)

def test_3(stamp):
    print(0)
    while True:
        flag=0
        while True:
            if gpio.input(foto):
                time.sleep(0.5)
                break
            if gpio.input(test3_full)==False:
                time.sleep(0.5)
                break
            gpio.output(led_paper, True)
            if flag==0:
                gpio.output(peeeep, True)
                time.sleep(3)
                gpio.output(peeeep, False)
                flag=1
        gpio.output(led_paper, False)
        test_2(stamp)
        time.sleep(3)
def go(mode_):
    if mode_==1:
        gpio.output(led_on_off, True)
        test_1_1()
        gpio.output(led_on_off, False)
    elif mode_==2:
        gpio.output(led_on_off, True)
        test_1_2()
        gpio.output(led_on_off, False)
    elif mode_==3:
        gpio.output(led_on_off, True)
        test_1_3()
        gpio.output(led_on_off, False)
    elif mode_==4:
        gpio.output(led_on_off, True)
        test_2(stamp)
        gpio.output(led_on_off, False)
    elif mode_==5:
        gpio.output(led_on_off, True)
        test_3(stamp)
        gpio.output(led_on_off, False)
while True:
    if gpio.input(test1_challenge1)==False:
        mode=1
        time.sleep(0.5)
    if gpio.input(test1_challenge2)==False:
        mode=2
        time.sleep(0.5)
    if gpio.input(test1_challenge3)==False:
        mode=3
        time.sleep(0.5)
    if gpio.input(test2)==False:
        mode=4
        time.sleep(0.5)
    if gpio.input(test3_full)==False:
        mode=5
        time.sleep(0.5)
    if gpio.input(stamp_print)==False:
        stamp=not(stamp)
        time.sleep(0.5)
    if stamp:
        gpio.output(led_print_stamp, True)
    else:
        gpio.output(led_print_stamp, False)
    if gpio.input(on_off)==False:
        time.sleep(1)
        with open('button.txt', 'w') as file:
            file.write('1')
        go(mode)
        with open('button.txt', 'w') as file:
            file.write('0')
