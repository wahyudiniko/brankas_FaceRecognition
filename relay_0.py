import RPi.GPIO as GPIO
from rpi_lcd import LCD 


relay = 21
lcd = LCD()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)

try:
	while True:
		lcd.text("RELAY NON AKTIF 0", 1)
		GPIO.output(relay, 0)

except KeyboardInterrupt:
	GPIO.cleanup()
	lcd.clear()
	pass

