#!/usr/bin/python

'''serial port connection to DAS.
string level sent
read serial and parse for response'''


import serial
import os
import time

ser = serial.Serial(port='/dev/ttyUSB0', timeout=4)
ser.write("level\n")
time.sleep(2)
print 'debug:',ser.inWaiting()
#s = ser.readlines()
#print 's',s

while ser.inWaiting() != 0:
    s = ser.readlines()
    print 's',s
    for i in s:
        if i.find('%') != -1:
            ind = i.find('%')
            print i[ind-4:ind+1], 'percent full'
            level = i[ind-4:ind+1]

#i = '33%'
#print i
f = open('/var/log/helium/log', 'r+')
f.seek(0,2)
f.write(time.ctime())
f.write(' : '+level+'\n')
f.close()
