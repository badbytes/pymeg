#       socket_talk.py
#
#       Copyright 2010 dan collins <danc@badbytes.net>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


'''client and server socket communication
s = socket_talk.setup()
s.server()
s.client('message2pass')
s.retrieve()'''

from socket import *


class setup:
    def __init__(self):
        pass

    def client(self,data, host='localhost', port=23456, buf=1024):
        '''host setup
        defines host address port and buffer size
        pass data by host(somedata)'''
        addr = (host,port);
        UDPSock = socket(AF_INET,SOCK_DGRAM)
        UDPSock.sendto(data,addr)
        #UDPSock.close()

    def server(self, host='localhost', port=23456, buf=1024):
        '''server setup
        defines host address port and buffer size'''
        addr = (host,port);
        self.UDPSock = socket(AF_INET,SOCK_DGRAM)
        self.UDPSock.bind(addr)
        self.buf = buf

    def retrieve(self, host='localhost', port=23456, buf=1024, timeout=1):
        self.UDPSock.settimeout(timeout)
        try:
            data,addr = self.UDPSock.recvfrom(buf)
            self.output = data
            #print self.output
            #print data
        except timeout:
            print('Timeout. No client socket data.')
        #UDPSock.close()
