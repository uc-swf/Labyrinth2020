# Fill BT Simulation file with random data
# for testing file read ...

import btsim as serial

SerialPort = "__RANDOM__"
bt = serial.Serial(SerialPort,115200)

bt.disableDelay()

fd=open("BTdata.txt","w")
line=""

for i in range(1,1000):
	line = bt.readline()
	line = line.replace(b'\r',b'')
	#print(line)
	fd.write(line.decode('utf-8'))	

fd.close()