import RPi.GPIO as GPIO
from rpi_lcd import LCD


lcd = LCD()
GPIO.setmode(GPIO.BCM)

MATRIX = [ [1, 2, 3, "A"],
	   [4, 5, 6, "B"],
           [7, 8, 9, "C"],
           ["*", 0, "#", "D"] ]

ROW = [5, 6, 13, 19]
COL = [16, 20, 21, 12]

lcd.text("NOMOR KEYPAD: ",1)

for j in range(4):
	GPIO.setup(COL[j], GPIO.OUT)
	GPIO.output(COL[j], 1)

for i in range(4):
	GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
	while True:
		for j in range(4):
			GPIO.output(COL[j], 0)

			for i in range(4):
				if GPIO.input(ROW[i]) == 0:
					print(MATRIX[i][j])
					lcd.text(str(MATRIX[i][j]), 2)
					while(GPIO.input(ROW[i])) == 0:
						pass
			GPIO.output(COL[j],1)

except KeyboardInterrupt:
	lcd.clear()
	GPIO.cleanup()
