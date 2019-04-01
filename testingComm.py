import BluetoothConnection
import time
comm =  BluetoothConnection.Bluetooth()
bt= comm.bluetooth
time.sleep(5)

counter = 0
while True:
	if counter%5 < 2:

		bt.write(str.encode('hi'))	
		print('sent hi')

	else:
		bt.write(str.encode("bye"))
		print('sent bye')
		
	
	
	print('now listening')
	print('this is the readline' + str(bt.readline()))
	#movingstate = bt.read(8)
	print('done listening')
	counter+=1
	print(counter)
	#print(movingstate)
	time.sleep(3)

