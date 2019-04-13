import BluetoothConnection
import time
comm =  BluetoothConnection.Bluetooth()
bt= comm.bluetooth
time.sleep(5)

counter = 0
while True:
	

	bt.write(str.encode('movingState'))	
	print('sent movingState')
		
	
	
	print('now listening')
	print('this is the readline' + str(bt.readline()))
	#movingstate = bt.read(8)
	print('done listening')
	counter+=1
	print(counter)
	#print(movingstate)
	time.sleep(3)

