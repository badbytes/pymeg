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
import sys
from numpy import arange,ceil,sqrt,shape,size
from gui.gtk import meg_assistant,errordialog
from meg import timef

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    print("GTK Not Availible")
    sys.exit(1)


class setup:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("timef.glade")
        self.window = self.builder.get_object("window")

        dic = {
            "on_button1_clicked" : self.apply_button,
            "on_filechooserbutton1_file_set" : self.read_data,
            #"on_filechooserbutton2_file_set" : self.save_data,
            }

        self.builder.connect_signals(dic)

    def errordialog(self, errormesg):
        error = errordialog.errorwin(errormesg)


    def apply_button(self,widget):
        print 'apply_button'
        print 'uri',self.builder.get_object('filechooserbutton1').get_uri()
        try:
            cycles = eval(self.builder.get_object("entry2").get_text())
            freqrange = eval(self.builder.get_object("entry3").get_text())
            padratio = eval(self.builder.get_object("entry4").get_text())
            timesout = eval(self.builder.get_object("entry5").get_text())
            frames = eval(self.builder.get_object("entry6").get_text())
            trials = eval(self.builder.get_object("entry7").get_text())
            srate = eval(self.builder.get_object("entry8").get_text())
            eventtime = eval(self.builder.get_object("entry9").get_text())
        except:
            print('not enough info. exiting')
            self.errordialog('not enough info. exiting');
            return -1

        print cycles,freqrange,padratio,timesout,frames,trials,srate,eventtime
        self.t = timef.initialize()

        try:
            chind = self.data_assist.pdfdata.data.channels.labellist.index(self.chan_sel)
            print 'chind',chind
            self.data2timef = self.data_assist.pdfdata.data.data_block[:,chind]
        except:
            print 'assuming data passed.'
        try:
            if self.data_selected == None: #not passing specific data
                try:
                    chind = self.workspace_data.data.channels.labellist.index(self.chan_sel)
                    self.data2timef = self.workspace_data.data.data_block[:,chind]
                except AttributeError:
                    pass
            else:
                print 'taking passed data'
                self.data2timef = self.data_selected[:,int(self.chan_sel)]
                print 'timef attempt'
        except AttributeError:
            print 'no data passed'


        print 'shape',self.data2timef.shape
        return_code = self.t.calc(data=self.data2timef,freqrange=freqrange,cycles=cycles,\
        padratio=int(padratio),timesout=int(timesout),frames=int(frames),\
        trials=int(trials),srate=float(srate),eventtime=int(eventtime))
        if return_code == -2:
            self.errordialog('Too few points in data for that freq range. Load more points or increase the min freq.');
        try:
            self.workspace_data.tft = self.t
        except AttributeError:
            self.builder.get_object('filechooserbutton2').set_uri(self.builder.get_object('filechooserbutton1').get_uri())
            self.builder.get_object('filechooserbutton2').show()
            self.builder.get_object('filechooserbutton2').set_state(True)


    def datahandler(self, workspace_data=None, data_selected=None):
        #print 'wd',workspace_data,data_selected
        self.workspace_data = workspace_data
        self.data_selected = data_selected
        self.check_data(None)

    def check_data(self,widget):
        print 'checking data'
        try:
            self.workspace_data
        except AttributeError:
            print 'data not passed'
            return
        if self.data_selected == None:
            #try:
            self.workspace_data.data.channels.labellist
            self.populate_combo(data_list = \
            self.workspace_data.data.channels.labellist)
            self.set_pdf_info(pdf_data=self.workspace_data)
            #except:
                #print 'no channels', size(self.workspace_data.shape),arange(size(self.workspace_data,1))
                #if size(self.workspace_data.shape) != 1:
                        #self.populate_combo(data_list = arange(size(self.workspace_data,1)))
                #print 'pass'
        else:
            print 'no channels', size(self.data_selected.shape),arange(size(self.data_selected,1))
            if size(self.data_selected.shape) != 1:
                self.populate_combo(data_list = arange(size(self.data_selected,1)))
            print 'pass'

    def read_data(self, widget):
        from time import sleep
        print 'reading data'
        from pdf2py import pdf, readwrite
        print self.builder.get_object('filechooserbutton1').get_uri()
        self.data_assist=meg_assistant.setup(path = \
        self.builder.get_object('filechooserbutton1').get_filename(),
        callback=self.callback)

    def callback(self):
        print 'DONE!'
        self.populate_combo(data_list = \
        self.data_assist.pdfdata.data.channels.labellist)
        self.set_pdf_info(pdf_data=self.data_assist.pdfdata)

    def set_pdf_info(self, pdf_data=None):
        self.builder.get_object("entry6").set_text\
        (str(pdf_data.data.data_block.shape[0]\
        /pdf_data.data.numofepochs[0]))
        self.builder.get_object("entry7").set_text\
        (str(pdf_data.data.numofepochs[0]))
        self.builder.get_object("entry8").set_text\
        (str(1/pdf_data.hdr.header_data.sample_period[0]))
        self.builder.get_object("entry9").set_text\
        (str(abs(pdf_data.data.eventtime[0])*1000))


    def populate_combo(self, data_list=None):
        print 'populating channel list'
        if data_list == None:
            data_list = ['None']#arange(50)
        combobox = self.builder.get_object("combobox1")
        liststore = gtk.ListStore(str)
        cell = gtk.CellRendererText()
        combobox.pack_start(cell)
        combobox.add_attribute(cell, 'text', 0)
        combobox.set_wrap_width(int(ceil(sqrt(len(data_list)))))

        for n in data_list: #range(50):
            liststore.append([n])
        combobox.set_model(liststore)
        combobox.connect('changed', self.changed_cb)
        combobox.set_active(0)
        return

    def changed_cb(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index > -1:
            print model[index][0], 'selected'
            self.chan_sel = str(model[index][0])
        return


if __name__ == "__main__":
    mainwindow = setup()
    mainwindow.window.show()
    print 'testing'
    gtk.main()
