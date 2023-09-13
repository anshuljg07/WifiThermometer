import time
import os
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)

from w1thermsensor import W1ThermSensor, Sensor

sensor = W1ThermSensor(Sensor.DS18B20)


'''
lcd_d7 = digitalio.DigitalInOut(board.D0)
lcd_d6 = digitalio.DigitalInOut(board.D5)
lcd_d5 = digitalio.DigitalInOut(board.D6)
lcd_d4 = digitalio.DigitalInOut(board.D13)
'''

lcd_columns=16
lcd_rows=2
lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
lcd.message=f'Temp (F):  \nTemp (C):  '



while True:
	try:
		temp_c = sensor.get_temperature()
		temp_f  = temp_c  *(9/5) + 32
		lcd.cursor_position(10,0)
		lcd.message = f'{temp_f}'
		lcd.cursor_position(10,1)
		lcd.message = f'{temp_c}'
		time.sleep(1)
	
	except Exception as e:
		print("not working")
		
	
	
	time.sleep(1) 
#lcd= GpioLCD(rs_pin=Pin(37), enable_pin=Pin(35), d4_pin=Pin(33), d5_pin=Pin(31), d6_pin=Pin(29), d7_pin=Pin(23), num_lines=2, numcolumns=16)

'''
#lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows = 2, pin_rs = 37, pin_e = 35, pins_data = [33, 31, 29, 23])
from w1thermsensor import W1ThermSensor, Sensor

sensor = W1ThermSensor(Sensor.DS18B20)

#lcd.cursor_pos = (0,0)
#lcd.write_string("Temp: ")

while True:
	temp_c = sensor.get_temperature()
	temp_f  = temp_c#  *(9/5) + 32
	print(f'{temp_f}\n')
	time.sleep(1) 

	
	lcd.cursor_pos = (0,0)
	lcd.write_string("Temp: " + temp_c + unichr(223) + "C")
	lcd.cursor_pos = (1,0)
	lcd.write_string("Temp: " + temp_f + unichr(223) + "F")
'''	
