import shlex, subprocess
from pathlib import Path
import time,serial


class Bluetooth():
	
	def __init__(self):
		bindFile = Path('/dev/rfcomm0')
		self.slowDownTrigger = False
		
		if not bindFile.exists():
			print("File doesn't exist, creating bind now")
			command = 'sudo rfcomm bind /dev/rfcomm0 98:D3:37:91:0F:BF 1'
			args = shlex.split(command)
			subprocess.Popen(args)
			time.sleep(2)
		else:
			print('Bind file exist')

		self.bluetooth = serial.Serial("/dev/rfcomm0",baudrate = 19200)

	#check to see if the car is moving
	def isMoving(self):
		command = "movingState"
		self.bluetooth.write(str.encode(command))
		time.sleep(1)
		movingState = self.bluetooth.read(8)
		print(movingState.decode('UTF-8',errors = 'replace'))
		print('this is the moving stat' +str(movingState))

		return movingState

	#send signal to RCcar to take over the driving
	def autoSlowDown(self):
		command = "sleeping"
		self.bluetooth.write(str.encode(command))
		self.slowDownTrigger = True
