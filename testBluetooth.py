
import serial,time,shlex,subprocess
'''

command = 'sudo rfcomm bind /dev/rfcomm0 98:D3:37:91:0F:BF 1'
args = shlex.split(command)
subprocess.Popen(args)
time.sleep(2)
'''
bluetooth = serial.Serial("/dev/rfcomm0",baudrate = 19200)
print('connected to the arduino')

data = 9
dat="hello<"
counter = 0
while True:
	if counter < 4:
		bluetooth.write(str.encode(dat))
		time.sleep(4)
		print(dat)
	else:
		bluetooth.write(str.encode('bye<'))
		print('bye')
		time.sleep(4)
	counter += 1
	print(counter)
