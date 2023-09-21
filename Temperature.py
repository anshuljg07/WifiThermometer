import time
import os
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
from w1thermsensor import W1ThermSensor, Sensor

from socketIO_client_nexus import SocketIO,LoggingNamespace #TODO: download this new package
from threading import Thread
import logging


def initHardware():
	lcd_rs = digitalio.DigitalInOut(board.D26)
	lcd_en = digitalio.DigitalInOut(board.D19)
	lcd_d7 = digitalio.DigitalInOut(board.D27)
	lcd_d6 = digitalio.DigitalInOut(board.D22)
	lcd_d5 = digitalio.DigitalInOut(board.D24)
	lcd_d4 = digitalio.DigitalInOut(board.D25)

	sensor = W1ThermSensor(Sensor.DS18B20)

	lcd_columns=16
	lcd_rows=2
	lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
	lcd.message=f'Temp (F):  \nTemp (C):  '

def updateLCDThread(tempf, tempc):
    lcd.cursor_position(10,0)
    lcd.message = f'{tempf}'
    lcd.cursor_position(10,1)
    lcd.message = f'{tempc}'
    time.sleep(1)

def transmitThread(tempf, tempc):
	payload = {
		'title': 'transmit temp',
		'temp_c': tempc,
		'temp_f': tempf
	}
	with SocketIO('localhost', 3000, LoggingNamespace) as socketIO:
		socketIO.emit('temp data', payload)
		socketIO.wait(seconds=1)


if __name__ == "__main__":
	initHardware()

	while True:
		time.sleep(1)
		try:
			temp_c = sensor.get_temperature()
			temp_f  = temp_c  *(9/5) + 32
			thread_lcd = Thread(target = updateLCDThread, args = (temp_f, temp_c, ))
			thread_transmit = Thread(target = transmitThread, args = (temp_f, temp_c, ))
			thread_lcd.start()
			thread_transmit.start()
			# updateLCDThread(temp_f, temp_c)
			# transmitThread(temp_f, temp_c)
		except Exception as e:
			print("not working")

#lcd= GpioLCD(rs_pin=Pin(37), enable_pin=Pin(35), d4_pin=Pin(33), d5_pin=Pin(31), d6_pin=Pin(29), d7_pin=Pin(23), num_lines=2, numcolumns=16)


