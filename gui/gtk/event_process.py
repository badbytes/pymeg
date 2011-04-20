#!/usr/bin/python2
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


import sys,os
from pdf2py import pdf,readwrite
from meg import trigger,event_logic,plot2dgtk,nearest, event_logic
from numpy import append,array,shape,ceil,sqrt

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

class setup_gui:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("window")
        self.statusbar = self.builder.get_object("statusbar")
        self.statusbar_cid = self.statusbar.get_context_id("")

        dic = {
            "on_button_delete_clicked" : self.event_delete,
            "on_filechooser_file_set" : self.get_trigger_events_from_data,
            "on_button_test_logic_clicked" : self.parse_logic,
            "on_menu_plot_events_activate" : self.plot_events,
            "showpopupmenu" : self.showpopupmenu,
            "on_get_event_list_activate" : self.show_event_list,
            "gtk_widget_hide" : self.hideinsteadofdelete,
            "on_button_process_clicked" : self.epoch_data,
            "on_text_changed" : self.check_status,
            "on_custom_trig_toggled" : self.populate_combo,
            "on_filter_and_add_clicked" : self.test,
            }

        self.builder.connect_signals(dic)
        self.updatestatusbar('Test logic of event prior to epoching/averaging')

    def test(self,widget):
        pass


    def updatestatusbar(self,string):
        self.statusbar.push(self.statusbar_cid, string)

    def check_status(self,widget):
        if self.builder.get_object("entry1").get_text() != '' and \
        self.builder.get_object("entry2").get_text() != '' and \
        self.builder.get_object("button1").is_sensitive() == True:
            self.builder.get_object("button4").set_sensitive(True)
            self.builder.get_object("button5").set_sensitive(True)
        else:
            self.builder.get_object("button4").set_sensitive(False)
            self.builder.get_object("button5").set_sensitive(False)


    def set_passed_filename(self, filepathstring, callback=None):
        self.callback = callback
        self.fnuri = 'file://'+filepathstring
        ###fixing oddity in set_uri, as char % needs to be set as %25 in filepath
        self.fnuri = self.fnuri.replace('%','%25')
        self.builder.get_object('filechooserbutton1').set_uri(self.fnuri)
        print 'recieved passed filename'

    def get_trigger_events_from_data(self,widget,channellabel=None):

        #p.data.setchannellabels(['Pinky','TRIGGER', 'RESPONSE'])

        print 'filename', self.builder.get_object('filechooserbutton1').get_uri()
        print(widget.get_filename())
        try:
            self.p = pdf.read(widget.get_filename()) #4D file read
            self.p.data.setchannels('trig') #datatype equals 'trigger'

            self.p.data.getdata(0, self.p.data.pnts_in_file) #read the whole file
            self.data = self.p.data.data_block #actual data array
            self.wintime = self.p.data.wintime #timecourse
            u,n,nz = trigger.vals(self.data) #u is the event value
            self.event_dict = event_logic.get_ind(u,self.data) #dictionary with indices to events

            for i in self.p.hdr.channel_ref_data:
                try: self.channellist = append(self.channellist, i.chan_label)
                except AttributeError: self.channellist = [i.chan_label]
            self.event_tree(None,u,self.event_dict,treeview='treeview1')
            self.builder.get_object('button1').set_sensitive(True)


        except TypeError:
            pass

    def set_selected_events_passed(self,widget,data,events,wintime):
        self.event_dict = {0:events}
        print 'passed event dict', self.event_dict
        self.event_tree(None,['1'],self.event_dict,treeview='treeview1')
        self.wintime = wintime
        self.data = data


    def event_tree(self,widget,event_list, event_dict, treeview):
        print('updating list')
        self.View = self.builder.get_object(treeview)
        self.liststore = gtk.ListStore(int,str,int,str)

        for k in event_dict.keys(): #range(1,5):
            event_val = event_list[k]
            num_events = len(event_dict[k])
            iter = self.liststore.append([k,str(event_val),num_events,event_val])
        self.View.set_model(self.liststore)

        try: self.colums_set
        except AttributeError:
            self.colums_set = True
            print('adding events')
            self.AddListColumn('Event Num', 0, self.View, self.liststore)
            self.AddListColumn('Event Val', 1, self.View, self.liststore)
            self.AddListColumn('Event Total', 2, self.View, self.liststore)
            self.AddListColumn('Logic Operation', 3, self.View, self.liststore, editable=True)


    def cell_edited_callback(self, path, new_text, user_data, model):
        liststore,iter = self.View.get_selection().get_selected_rows()
        liststore[iter[0][0]][3] = user_data
        return

    def event_delete(self, widget):
        liststore,iter = self.View.get_selection().get_selected()
        liststore.remove(iter)


    def AddListColumn(self, title, columnId, viewtype, model, editable=False):
        renderer = gtk.CellRendererText()
        if editable == True:
            renderer.connect('edited', self.cell_edited_callback, model)
            renderer.set_property('editable', True)
        column = gtk.TreeViewColumn(title,renderer,text=columnId)
        column.set_resizable(True)
        column.set_sort_column_id(columnId)
        viewtype.append_column(column)
        viewtype.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

    def parse_logic(self,widget):
        self.result_all_ind = array([])
        '''8192>4216,300ms'''
        liststore,iter = self.View.get_selection().get_selected_rows()
        logic_list = []
        for i in iter:
            logic_list.extend([liststore[i[0]][3]])
        #logic = liststore[iter[0][0]][3]
        print 'logic found',logic_list

        for logic in logic_list:
            trig_vals = logic.split(',')[0].split('>')
            try: timediff = int(logic.split(',')[1].rstrip('ms'))
            except: timediff = 0


            trig_int = []
            for i in trig_vals: #strings to integers
                trig_int.append(int(i))

            self.ind_dict = event_logic.get_ind(trig_int,self.data)
            print('indices dict',self.ind_dict)

            if len(self.ind_dict.keys()) == 1:
                self.result_ind = self.ind_dict[0]
                print('result',self.result_ind)
            else:
                self.result_ind = event_logic.ind_logic(self.ind_dict, timediff, self.wintime)
                print(self.result_ind,'timediff',timediff)

            try:
                self.result_all_ind = append(self.result_all_ind,self.result_ind)
            except AttributeError:
                self.result_all_ind = self.result_ind

        print self.result_all_ind

        self.updatestatusbar('Logic Result: '+str(len(self.result_all_ind))+' events passed conditions')
        self.check_status(None)


    def plot_events(self,widget):
        print shape(self.data),shape(self.wintime)
        plot2dgtk.makewin(self.data,self.wintime)#,plottype='imshow')

    def showpopupmenu(self,widget,event):
        print('button ',event.button)
        if event.button == 3:
            m = self.builder.get_object("menu1")
            print(widget, event)
            m.show_all()
            m.popup(None,None,None,3,0)

    def show_event_list(self,widget):
        print 'trying'
        event_list_win = self.builder.get_object("window1")
        event_list_win.show()
        liststore = gtk.ListStore(int,str)
        View = self.builder.get_object("treeview2")

        if View.get_columns() == []:
            self.colums_set = True
            self.AddListColumn('Time', 0, View, liststore)
            self.AddListColumn('Event Onset', 1, View, liststore)
            View.set_model(liststore)

        for i in self.event_dict.keys():
            for j in self.event_dict[i]:

                liststore.append([i,str(self.wintime[j])])
        View.set_model(liststore)


    def epoch_data(self,widget):
        print widget.get_label()
        prestim_sec = float(self.builder.get_object("entry1").get_text())
        poststim_sec = float(self.builder.get_object("entry2").get_text())
        prestim_ind = nearest.nearest(self.wintime,prestim_sec)[0]
        poststim_ind = nearest.nearest(self.wintime,poststim_sec)[0]
        #print prestim_ms,poststim_ms

        print 'epoch'
        startcut = self.result_ind-prestim_ind
        endcut = self.result_ind+poststim_ind
        self.callback(widget,startcut,endcut)
        return
        epoched = self.data[self.result_ind-prestim_ind:self.result_ind+poststim_ind]
        print epoched.shape,'shape'

    def populate_combo(self,widget):
        if self.builder.get_object("togglebutton1").get_active():
            self.builder.get_object("hbox2").set_visible(True)
        else:
            self.builder.get_object("hbox2").set_visible(False)
            return

        channellist = self.channellist
        print 'populating channel list'
        if channellist == None:
            data_list = ['None']#arange(50)
        combobox = self.builder.get_object("combobox1")

        combobox.clear()
        liststore = gtk.ListStore(str)
        cell = gtk.CellRendererText()
        combobox.pack_start(cell)
        combobox.add_attribute(cell, 'text', 0)
        combobox.set_wrap_width(int(ceil(sqrt(len(channellist)))))

        for n in channellist: #range(50):
            liststore.append([n])
        combobox.set_model(liststore)
        combobox.connect('changed', self.changed_cb)
        combobox.set_active(0)
        return

    def changed_cb(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index > -1:
            #print model[index][0], 'selected'
            self.chan_sel = str(model[index][0])
        return

    def hideinsteadofdelete(self,widget, ev=None):
        widget.hide()
        return True

    def custom_trig_detect(self,widget):
        win = float(self.builder.get_object("entry3").get_text())
        slide = float(self.builder.get_object("entry4").get_text())
        thresh = float(self.builder.get_object("entry3").get_text())
        p.data.setchannellabels([])
        trigger.event_detection()




if __name__ == "__main__":
    mainwindow = setup_gui()
    mainwindow.window.show()
    fn = '/home/danc/programming/python/data/0611/0611piez/e,rfhp1.0Hz,COH'
    mainwindow.set_passed_filename(fn)
    gtk.main()
