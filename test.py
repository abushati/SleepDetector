import BluetoothConnection

var = BluetoothConnection.Bluetooth()
flag = 1
print(var.slowDownTrigger)
if flag > 0 and not var.slowDownTrigger:

	print("the first if statement worked" + var.slowDownTrigger)

var.autoSlowDown()
print(var.slowDownTrigger)

if flag > 0 and not var.slowDownTrigger:

        print('the second one worked'+ var.slowDownTrigger)
print(var.slowDownTrigger)
