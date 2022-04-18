'''
Serial port starter code
EE445L Lab 10 option
April 12, 2022
Jon Valvano
'''
#from command line
#py -m pip install pyserial
#py -m pip install matplotlib

import serial
import matplotlib.pyplot as plt
import time
from time import sleep
time =  [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
speed = [5, 6, 4, 4, 5, 6, 4, 4, 5, 5]
plt.ylabel('Speed (rps)')
plt.xlabel('Time (sec)')
if not plt.isinteractive():
	plt.interactive(True)
#fig = plt.figure()
plt.show()
from serial import Serial
ser = serial.Serial('COM5', 115200)
print('Connected to',ser.name)             # check which port was really used
print('Baud rate',ser.baudrate,'bits/sec') # baud rate

serialString = ""                          # Used to hold data coming over UART
command = ""
valuestr = ""
value = 0
ser.timeout = 1
currentSpeed = 0
KP1 = 0
KP2 = 0
KI1 = 0
KI2 = 0
while command != 'q': #Main loop
    print("Current Rotations Per Second: " + str(currentSpeed))
    print("Current KP1: " + str(KP1))
    print("Current KP2: " + str(KP2))
    print("Current KI1: " + str(KI1))
    print("Current KI2: " + str(KI2))
    print()
    command = input("Command>")

    if command == "S":
        valuestr = input("New Rotations Per Second=")
        newSpeed = int(valuestr)
        print("Setting RPS to: " + str(newSpeed))
        currentSpeed = newSpeed
        ser.write('S'.encode('ASCII'))
        ser.write(valuestr.encode('ASCII'))
        ser.write('\r'.encode('ASCII'))
    if command == "K":
		# We need P or I and then 1 or 2
        module = input("Which Module? Choose P or I: ")
        whichK = int(input("Which K? Chose 1 or 2: "))
        val = input("New K" + str(module) + str(whichK) + "= ")
        if(module == 'P' and whichK == 1):
            KP1 = int(val)
        elif(module == 'P' and whichK == 2):
            KP2 = int(val)
        elif(module == "I" and whichK == 1):
            KI1 = int(val)
        elif(module == "I" and whichK == 2):
            KI2 = int(val)
        print("Setting K" + str(module) + str(whichK) + " to: " + val)
        ser.write('K'.encode('ASCII'))
        sleep(0.1)
        ser.write(module.encode('ASCII'))
        sleep(0.1)
        ser.write(str(whichK).encode('ASCII'))
        sleep(0.1)
        ser.write(val.encode('ASCII'))
        ser.write('\r'.encode('ASCII'))
    if command == "L":
        valuestr = input("Value=")
        value = int(valuestr)
        print("LED =",value)
        ser.write('L'.encode('ASCII'))
        ser.write(valuestr.encode('ASCII'))
        ser.write('\r'.encode('ASCII'))
    if command == "l":
        print("LED off")
        ser.write('l'.encode('ASCII'))
    if command == "R":
        print("Run")
        ser.write('R'.encode('ASCII'))
        sleep(2.0)
        serialString = ser.readline(1000)
        print (serialString)
        speed = [int(s) for s in serialString.split() if s.isdigit()]
        print (speed)
        plt.clf()
        plt.plot(time,speed)
    print()
