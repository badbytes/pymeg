#!/usr/bin/python2
#!/usr/bin/env python


#       dbswitcher.py
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
#!/usr/bin/env python


import pygtk
pygtk.require('2.0')
import gtk, gtk.glade

import subprocess, os, sys


class cbtest:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("AdvancedCoilEditor.glade")
        self.window = self.builder.get_object("window1")
        self.window.show()
        store = gtk.ListStore(str)
        store.append(["Choose a Database"])
        dic = {
            "on_button1_clicked" : self.getposted,
            "on_button2_clicked" : self.transform,
            }
        self.builder.connect_signals(dic)

        self.getposted(None)

        self.builder.get_object("combobox1").set_active(0)
        self.builder.get_object("combobox2").set_active(1)
        self.builder.get_object("combobox3").set_active(2)
        self.builder.get_object("combobox4").set_active(3)
        self.builder.get_object("combobox5").set_active(4)
        stage = os.environ['STAGE']
        self.builder.get_object("filechooserbutton1").set_current_folder(stage+'/config/')
        
        for i in sys.path:
            p = i.find('pymeg')
            if p > 0:
                path2config = i.split('pymeg')[0]+'pymeg/config/'
                f = open(path2config+os.listdir(path2config)[0])
                self.conf = f.readline().split('.')[0]
                print 'default config set to:',self.conf
                self.builder.get_object("filechooserbutton1").set_uri('file:///'+stage+'/config/'+self.conf+'.config')
                return
            else:
                print 'no default configuration file set'
        

    def getposted(self,widget):
        s = subprocess.Popen('get_posted_sel', shell=True, stdout=subprocess.PIPE)
        out = s.stdout.readlines()
        print out
        #self.builder.get_object("label1").set_label(out[0])
        s = subprocess.Popen('get_PSsrp', shell=True, stdout=subprocess.PIPE)
        self.post = s.stdout.readlines()
        print 'posted',self.post
        self.builder.get_object("label1").set_text(self.post[0])

    def transform(self, widget):
        
        #self.builder.get_object("combobox1").set_active(4)
        c1 = self.builder.get_object("combobox1").get_active_text()
        c2 = self.builder.get_object("combobox2").get_active_text()
        c3 = self.builder.get_object("combobox3").get_active_text()
        c4 = self.builder.get_object("combobox4").get_active_text()
        c5 = self.builder.get_object("combobox5").get_active_text()
        coilorder=(c1 + "," + c2 +  "," + c3 +  "," + c4 +  "," + c5)
        chan2del = self.builder.get_object("entry1").get_text()
        trans = '1'
        cmd2run = "calc_coil_pos " + " -C " + self.conf +'  '+ self.post[0].split('\n')[0] + " -X " + trans + " -O " + coilorder + " -I " + chan2del + " -f"
        #os.system("calc_coil_pos " + " -C " + self.conf +'  '+ self.post[0] + " -X " + trans + " -O " + coilorder + " -I " + chan2del + " -f" )
        os.system(cmd2run)
        print cmd2run

    def on_window1_destroy(self,w):
        gtk.main_quit()

if __name__ == "__main__":
    cbtest()
    gtk.main()
