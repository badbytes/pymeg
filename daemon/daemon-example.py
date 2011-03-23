#!/usr/bin/env python

import sys, time, os
from daemon import Daemon
import serial

class MyDaemon(Daemon):
    
    def run(self):
        #f = open('/tmp/test.txt', 'w')
        while True:
            #ser = serial.Serial(port='/dev/ttyUSB0', timeout=1)
            #ser.write("level\n")
            #s=ser.readlines()
            #x=s[1].split('=')[1].split('%')[0].lstrip()
            #return x

            '''
            startacq PID TEMPLATE 
            stopacq
            status
            
            '''
            time.sleep(1)
            try:
                self.f = open('/tmp/test.txt', 'r+')
            except IOError:
                self.f = open('/tmp/test.txt', 'w+')
            self.f.seek(0, os.SEEK_END)
            self.f.write('i')
            
            #self.f.flush()
            
            print self.f.tell(),'test'
            self.f.close()

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
