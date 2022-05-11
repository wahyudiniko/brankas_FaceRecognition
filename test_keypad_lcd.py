#!/usr/bin/python3

import RPi.GPIO as GPIO
from rpi_lcd import LCD
import time
import os


lcd = LCD()

L1 = 5 
L2 = 6
L3 = 13
L4 = 19
C1 = 16
C2 = 20
C3 = 21
C4 = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        os.system("clear")
        print(ord(characters[0]))
    if(GPIO.input(C2) == 1):
        print(ord(characters[1]))
    if(GPIO.input(C3) == 1):
        print(ord(characters[2]))
    if(GPIO.input(C4) == 1):
        print(ord(characters[3]))
    GPIO.output(line, GPIO.LOW)

try:
    while True:
        readLine(L1, ["1","2","3","A"])
        readLine(L2, ["4","5","6","B"])
        readLine(L3, ["7","8","9","C"])
        readLine(L4, ["*","0","#","D"])
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\nProgram is stopped")
