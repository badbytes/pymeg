#!/usr/bin/env python

import sys, time, os
from daemon import Daemon
import serial
import subprocess

class MyDaemon(Daemon):
    def run(self):
        #socat PTY,link=$HOME/COM1 PTY,link=$HOME/COM2
        serport = '/dev/ttyS0'
        #serport = '/home/danc/COM2'
        ser = serial.Serial(port=serport, timeout=1)
        #if ser.isOpen() != True:
            #time.sleep(10)
        #else:
        while True:
            time.sleep(.1)
            command = ser.readline()#.strip('\n') #read one line (make sure sender puts newline break at end of line)
            if command != '':
                reply = self.interpreter(command)
                ser.write(reply+'\n')
            #else:
                #ser.write('I have nothing to say dave.\n')

    def interpreter(self, command):
            '''api...
            hello -> ask if server alive
            startacq pid template-> ask acquisition to start
            stopacq -> stop acq
            '''
            if command[-1] == '\r':
                command = command.split('\r')[0]+'\n'

            cmd = command.split(' ')

            #for i in cmd:
            print cmd
            self.writelog(command, 'receive')
            if cmd[0] == 'hello\n':
                resp = 'how can i help you dave?'
            elif cmd[0] == 'help\n':
                resp = 'type command: help startacq, help stopacq, help status'
            elif cmd[0] == 'help':
                if cmd[1] == 'startacq\n':
                    resp = 'startacq 0001 Aud40hz, (startacq PID TEMPLATE) OR, startacq posted Aud40hz'
                elif cmd[1] == 'stopacq\n':
                    resp = 'command stopacq will stop current acquisition'
                elif cmd[1] == 'status\n':
                    resp = 'return current state of acquisition machine'

            elif cmd[0] == 'status\n':
                stat = self.acqstatus()
                resp = stat
                self.writelog('RESPONSE:'+resp+'\n', 'receive')
            elif cmd[0] == 'trialnum\n':
                pass
            elif cmd[0] == 'log\n':
                self.writelog(cmd[1]+'\n', 'receive')
            elif cmd[0] == 'debug\n':
                self.writelog('debug:'+cmd[1],'debug')

            elif cmd[0] == 'startacq':
                stat = self.acqstatus()
                if stat == 'currently acquiring data':#\n':
                    resp = 'i cannot do that dave. data acquisition is already in progress. stopacq first'
                else:
                    if cmd[1] == 'posted':
                        p = subprocess.Popen('get_posted_sel', stdout=subprocess.PIPE)#;out = p.stdout.readlines()
                        p.poll()
                        out = p.stdout.readline()
                        PID = out.split()[0].split('@')[0]
                        #PID = out[0].split('@')[0]
                    else:
                        PID = cmd[1]
                    try:
                        RUN = cmd[3].split('\n')[0]
                    except:
                        pass
                    self.writelog(PID, 'receive')
                    TEMPLATE = cmd[2].split('\n')[0]
                    self.writelog(TEMPLATE, 'receive')
                    self.writelog(RUN, 'receive')
                    try:
                        resp = 'ok, starting acquisition on PID '+PID+' on template '+TEMPLATE+' for run '+RUN
                    except:
                        pass
                    #aip -m data0 -v A1 -C Colorado_Jan2010 -P phantom -S SEF -s '07/23/09 11:02' -r 2 -q

                    #if RUN == '1':
                    currenttime = self.datenow()
                    self.ct = currenttime

                    #else: #use current session
                    #    currenttime = self.ct

                    #resp = self.datenow()
                    try:
                        #os.system('ape')
                        #stat = os.system('aip -m data0 -v A1 -C Colorado_June2010 -P '+PID+' -S '+TEMPLATE+\
                        #' -s '+currenttime+' -r '+RUN+' -q')

                        stat = subprocess.Popen(['aip', '-m', 'data0', '-v', 'DC_SUB+frontline', '-C', 'Colorado_June2010', '-P', PID,'-S',TEMPLATE,'-s',currenttime,'-r',RUN,'-q','-c 5'], stdout=subprocess.PIPE)
                        self.writelog('aip -m data0 -v DC_SUB+frontline -C Colorado_June2010 -P'+PID+'-S'+TEMPLATE+'-s'+currenttime+'-r'+RUN+'-q'+'-c 5', 'receive')
                        stat.poll()
                        if stat.returncode == 2:
                            #if stat.stdout.readlines([0].index('Database record not found'))
                            resp = 'database record not found. check your template and that the patient exists.'
                        if stat.returncode == 6:
                            resp = 'run exists'
                        if stat.returncode == -11:
                            resp ='Cannot open system configuration file'
                    except:
                        resp = 'something went wrong dave. initialization crashed'
            elif cmd[0] == 'stopacq\n':
                stat = self.acqstatus()
                if stat == 'no data being acquired':
                    resp = 'i cannot do that dave. no data is being acquired'
                else:
                    resp = 'stopping acquisition '+self.pid
                    os.system('kill -15 '+self.pid)
            else:
                resp = 'dont know what you want me to do dave? Try typing: help'
            return resp

    def acqstatus(self):
        for line in os.popen("ps xa"):
            fields  = line.split()
            process = fields[4]
            if process == 'pci_data_transfer':# or process == 'aip':
                resp = 'currently acquiring data'
                self.pid = fields[0]
                self.writelog(self.pid, 'receive')
                return resp
            #else:
                #resp = 'no data being acquired'
                #self.pid = 'noid'
                #self.writelog(self.pid, 'receive')
                #return resp

        try:
            resp
        except NameError:
            self.pid = 'noid'
            resp = 'no data being acquired'
            return resp

    def datenow(self):
        import datetime
        now = datetime.datetime.now()
        if len(str(now.minute)) == 1:
            minute = '0'+str(now.minute)
        else:
            minute = str(now.minute)
        return str(now.month)+'/'+str(now.day)+'/'+str(now.year)[-2:]+' '+str(now.hour)+':'+minute

    def writelog(self, logcmd, direction):
            #time.sleep(1)
            try:
                self.f = open('/tmp/'+direction+'.txt', 'r+')
            except IOError:
                self.f = open('/tmp/'+direction+'.txt', 'w+')
            self.f.seek(0, os.SEEK_END)
            self.f.write(logcmd)
            self.f.close()

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/stimcontrol.pid')
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



'''
 aip -m data0 -v A1 -C Colorado_June2010 -P TEST -S A1 -s '01/01/01 01:01' -r 1 -q -R 'test comment' -w -d -H -I -q

use: aip [-P patient -S scan -s session -r run | [-P patient] -S scan] [-q] [-w] [-d] [-C config_file ] [-m file_system] [-a {x,y,z}offset] [-z trace_flags] [-D] [-x] [-o] [-c #_of_coils,[coh_prompt]] [-H] [-I] [-R run_comment_text_file] [-K weight file] [-E analog,high,low,gradient] [-M montage_file] [-v video_setup]

-q      quiet mode (not implemented)
     -w     do not display window (not implemented)
     -d     debug mode
     -C config  config file (default is set by APE)
     -m FileSystem  data partition
     -a {x,y,z}offset
            analog offset for x, y, or z direction
     -z trace   hex trace flags for debugging
     -x     turn on message tracing
     -o     (attempt to) overwrite an existing run
     -c coils   turn COH off (coils == 0) or on (coils from 3 to 16)
      [coh_prompt]   1 to prompt for the first COH acquisition;
                     2 for the verification;  3 for both;  0 for none(default)
     -E     0 to turn of analog, high gain, low gain, and gradiometer weights
     -G     display GUI only; do not talk to DAS
     -H     detailed help
     -I     send as idle parameters
     -K     weight table
     -M     montage file
     -v     video setup file
     -R file    run comments text file
'''
