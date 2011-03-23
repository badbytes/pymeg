#       text2speech.py
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


#from http://hakki.cornelii.org/quick_py_tts.html
import os

BIN="/usr/bin/festival"

    
class Festival(object):
    def __init__(self):
        if os.path.exists(BIN) == False:
            print 'festival not installed. sudo apt-get install festival'
            return
        
        self.p = os.popen("%s --pipe" % BIN, "w")

    def eval(self, scm):
        self.p.write(scm + "\n")
        self.p.flush()

    def say(self, text):
        text = text.replace('"', '')
        self.eval('(SayText "%s")' % str(text))

    
