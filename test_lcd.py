#!/usr/bin/python3

import RPi.GPIO as GPIO
from rpi_lcd import LCD
import time


buzzer = 4
ledRed = 16
ledGreen = 20
relay = 21
lcd = LCD()
t = 1 #delay

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)
GPIO.setup(relay, GPIO.OUT)


try:
	while True:
		lcd.text("relay aktif", 1)
		lcd.text("0", 2)
		GPIO.output(buzzer, 1)
		GPIO.output(ledRed, 0)
		GPIO.output(ledGreen, 1)
		GPIO.output(relay, 0)
		time.sleep(t)
		lcd.clear()

		lcd.text("relay non aktif", 1)
		lcd.text("1", 2)
		GPIO.output(buzzer, 0)
		GPIO.output(ledRed, 1)
		GPIO.output(ledGreen, 0)
		GPIO.output(relay, 1)
		time.sleep(t)
		lcd.clear()

except KeyboardInterrupt:
	GPIO.cleanup()
	lcd.clear()
	pass


