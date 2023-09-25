import time
from twilio.rest import Client as smsClient
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
from w1thermsensor import W1ThermSensor, Sensor


#from socketIO_client_nexus import SocketIO,LoggingNamespace #TODO: download this new package
from socketio import Client
from threading import Thread
import logging

sensor = W1ThermSensor(Sensor.DS18B20)
sio = Client()

#phone number shit 
#account_sid = os.environ['ACd7d90d03508c25c4e2b171168bff40be']
#auth_token = os.environ[]
smsClient = smsClient('ACd7d90d03508c25c4e2b171168bff40be','c2d3f36c8d94d1bacfbb4ed8399b9353')

message = smsClient.messages.create(
		body='Test',
		from_='+18665165495',
		to='+13198550125'
		)
		
print(message.sid)
#end of phone number 



def initHardware():
	lcd_rs = digitalio.DigitalInOut(board.D26)
	lcd_en = digitalio.DigitalInOut(board.D19)
	lcd_d7 = digitalio.DigitalInOut(board.D27)
	lcd_d6 = digitalio.DigitalInOut(board.D22)
	lcd_d5 = digitalio.DigitalInOut(board.D24)
	lcd_d4 = digitalio.DigitalInOut(board.D25)

	

	lcd_columns=16
	lcd_rows=2
	lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
	lcd.message=f'Temp (F):  \nTemp (C):  '
	return lcd

def updateLCDThread(lcd, tempf, tempc):
    lcd.cursor_position(10,0)
    lcd.message = f'{tempf}'
    lcd.cursor_position(10,1)
    lcd.message = f'{tempc}'

def transmitThread(tempf, tempc):
	payload = {
		'title': 'transmit temp',
		'temp_c': tempc,
		'temp_f': tempf
	}
	sio.emit('temp data', payload)
	'''
	print("Attempting Connection")
	with SocketIO('172.17.7.178', 3000, LoggingNamespace) as socketIO:
		print("Connected")
		socketIO.emit('temp data', payload)
		print('Sent Data: ', payload)
		#socketIO.wait(seconds=1)
	print("Finished Connection")
	'''
@sio.on('connect')
def on_connect():
	print('Connected')

if __name__ == "__main__":
	lcd = initHardware()
	sio.connect('http://172.17.7.178:3000')

	#TODO: Test new socket identifier
	sio.emit('clientType').emit('raspberryPi')

	while True:
		time.sleep(1)
		try:
			temp_c = sensor.get_temperature()
			temp_f  = temp_c  *(9/5) + 32
			thread_lcd = Thread(target = updateLCDThread, args = (lcd, temp_f, temp_c, ))
			thread_transmit = Thread(target = transmitThread, args = (temp_f, temp_c, ))
			thread_lcd.start()
			thread_transmit.start()
			# updateLCDThread(temp_f, temp_c)
			# transmitThread(temp_f, temp_c)
		except Exception as e:
			print(e)
			print("not working")
	sio.disconnect()

#lcd= GpioLCD(rs_pin=Pin(37), enable_pin=Pin(35), d4_pin=Pin(33), d5_pin=Pin(31), d6_pin=Pin(29), d7_pin=Pin(23), num_lines=2, numcolumns=16)


