import os
import time
import RPi.GPIO as gpio
import sys
on_off=14
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
os.system("pgrep -f Programm_very_important.py>>PID_stop.txt")
time.sleep(0.5)
while True:
    gpio.setmode(gpio.BCM)
    gpio.setup(on_off, gpio.IN)
    if gpio.input(on_off)==False:
        with open('button.txt', 'r') as file:
            button=file.readline()[0]
        if button=='0':
            time.sleep(1.5)
            continue
        else:
            print("AAAAA Women")
            with open('PID_stop.txt', 'r') as file:
                for i in file.readlines():
                    try:
                        print(int(i))
                        os.kill(int(i), 9)
                    except:
                        continue
            os.remove('PID_stop.txt')
            gpio.cleanup()
            print("AAAAA Men")
            break