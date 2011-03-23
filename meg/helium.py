import serial
import os
stage = os.environ['STAGE']
##def read():
ser = serial.Serial(port='/dev/ttyUSB0', timeout=1)
ser.write("level\n")
s = ser.readlines()
#print s
f = open(stage+'/map/log/helium_log')
r = f.readlines()
lev = r[-1].split("\t")
print lev
#x=s[1].split('=')[1].split('%')[0].lstrip()
#print x
#return x

if __name__ == '__main__':
    pass
    #l = read()
    #print l

