import time
from twilio.rest import Client as smsClient
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
from w1thermsensor import W1ThermSensor, Sensor
from datetime import datetime


#from socketIO_client_nexus import SocketIO,LoggingNamespace #TODO: download this new package
from socketio import Client
from threading import Thread, Event
import logging

sio = Client()
boolMasterSwitch = True
global sensor


'''
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
'''
@sio.on('connect')
def on_connect():
	print('Connected')

@sio.on('*')
def catch_all_server(event, data):
	global boolMasterSwitch
	if event == 'master switch state':
		print(data)
		print('type is :',type(data['masterSwitchState']))
		boolMasterSwitch = bool(data['masterSwitchState'])
		

'''	
@sio.on('master switch state')
def on_masterSwitchState():
	print("Master switch state received")
'''

	


def transmitSensorDisconnected  (event: Event) -> None:
	while(True):
		if event.is_set():
			break
		timestamp = datetime.now()
		strtime = timestamp.strftime("%H:%M:%S")
		payload = {
		'title': 'Sensor Disconnected',
		'temp_c': 'Sensor Disconnected',
		'temp_f': 'Sensor Disconnected',
		'timestamp' : strtime
		}
		
		sio.emit('temp data', payload)
		time.sleep(1)

def initHardware():
	lcd_rs = digitalio.DigitalInOut(board.D26)
	lcd_en = digitalio.DigitalInOut(board.D19)
	lcd_d7 = digitalio.DigitalInOut(board.D27)
	lcd_d6 = digitalio.DigitalInOut(board.D22)
	lcd_d5 = digitalio.DigitalInOut(board.D24)
	lcd_d4 = digitalio.DigitalInOut(board.D25)
	
	lcd_rs.direction = digitalio.Direction.OUTPUT
	lcd_en.direction = digitalio.Direction.OUTPUT
	lcd_d7.direction = digitalio.Direction.OUTPUT
	lcd_d6.direction = digitalio.Direction.OUTPUT
	lcd_d5.direction = digitalio.Direction.OUTPUT
	lcd_d4.direction = digitalio.Direction.OUTPUT
	
	#create physical switch input D14
	physicalSwitchPin = digitalio.DigitalInOut(board.D14)
	physicalSwitchPin.direction = digitalio.Direction.INPUT
	
	#create physical button input D23
	physicalButtonPin = digitalio.DigitalInOut(board.D23)
	physicalButtonPin.direction = digitalio.Direction.INPUT
	

	
	
	
	print('inside init')
	lcd_columns=16
	lcd_rows=2
	lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
	lcd.message=f'Temp (F):  \nTemp (C):  '
	return lcd, physicalSwitchPin.value, physicalButtonPin.value

def updateLCDThread(lcd, tempf, tempc):
    lcd.cursor_position(10,0)
    lcd.message = f'{tempf}'
    lcd.cursor_position(10,1)
    lcd.message = f'{tempc}'

def transmitThread(tempf, tempc, transmitNull):
	timestamp = datetime.now()
	strtime = timestamp.strftime("%H:%M:%S")
	
	
	if transmitNull:
		payload = {
		'title': 'transmit temp',
		'temp_c': tempc,
		'temp_f': tempf,
		'timestamp' : strtime
		}
	else:
		payload = {
		'title': 'transmit temp',
		'temp_c': 'NO DATA AVAILABLE',
		'temp_f': 'NO DATA AVAILABLE',
		'timestamp' : strtime
		}
		
	sio.emit('temp data', payload)

def connectDS18B20():
	tempsensor = None
	try:
		tempsensor = W1ThermSensor(Sensor.DS18B20)
		return tempsensor
	except Exception as e:
		event = Event()
		sensorDisconnectedThread = Thread(target = transmitSensorDisconnected, args = (event,))
		sensorDisconnectedThread.start()
		while(tempsensor is None):
			try:
				tempsensor = W1ThermSensor(Sensor.DS18B20)
				event.set()
				return tempsensor
			except:
				print("Trying to connect to DS18B20")
	'''
	print("Attempting Connection")
	with SocketIO('172.17.7.178', 3000, LoggingNamespace) as socketIO:
		print("Connected")
		socketIO.emit('temp data', payload)
		print('Sent Data: ', payload)
		#socketIO.wait(seconds=1)
	print("Finished Connection")
	'''
	

if __name__ == "__main__":
	sio.connect('http://172.17.66.142:3000')
	sio.emit('clientType', 'raspberryPi')
	
	LCDPowerPin = digitalio.DigitalInOut(board.D13)
	LCDPowerPin.direction = digitalio.Direction.OUTPUT

	
	LCDPowerPin.value = 1
	lcd, boolSwitch, boolButton = initHardware()

	while True:
		sensor = connectDS18B20()
		time.sleep(1)
		try:
			#print(boolMasterSwitch)
			temp_c = sensor.get_temperature()
			temp_f  = temp_c  *(9/5) + 32
			
			lcd, boolSwitch, boolButton = initHardware()
			
			LCDPowerPin.value = 1
			print('bool switch:', boolSwitch, '\tboolButton:', boolButton, '\tLCDPowerpin', LCDPowerPin.value)
			
			
			
			#Master switch & physical switch & Button must be True for LCD
			if(boolMasterSwitch and boolSwitch and boolButton):
				print('displaying on LCD')
				thread_lcd = Thread(target = updateLCDThread, args = (lcd, temp_f, temp_c, ))
				thread_lcd.start()
			else:
				pass
				#LCDPowerPin.value = False
			
			#Sending ANY Temperature data Physical Switch & Master Switch must be True
				#else send NO DATA AVAILABLE in temp fields of JSON
			if(boolMasterSwitch and boolSwitch):
				
				thread_transmit = Thread(target = transmitThread, args = (temp_f, temp_c, True, ))
			else:
				thread_transmit = Thread(target = transmitThread, args = (temp_f, temp_c, False, ))
				
			
			#thread_lcd.start()
			thread_transmit.start()
			# updateLCDThread(temp_f, temp_c)
			# transmitThread(temp_f, temp_c)
		except Exception as e:
			print(e)
			print("not working")
	sio.disconnect()


#lcd= GpioLCD(rs_pin=Pin(37), enable_pin=Pin(35), d4_pin=Pin(33), d5_pin=Pin(31), d6_pin=Pin(29), d7_pin=Pin(23), num_lines=2, numcolumns=16)


