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
from pdf2py import pdf
from meg import trigger,event_logic,plot2dgtk

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
        self.builder.add_from_file("event_process.glade")
        self.window = self.builder.get_object("window")

        dic = {
            "on_button1_clicked" : self.test,
            "on_button_delete_clicked" : self.event_delete,
            "on_filechooser_file_set" : self.get_trigger_events_from_data,
            "on_button_test_logic_clicked" : self.parse_logic,
            "on_menu_plot_events_activate" : self.plot_events,
            "showpopupmenu" : self.showpopupmenu,
            "on_get_event_list_activate" : self.show_event_list,
            "gtk_widget_hide" : self.hideinsteadofdelete,
            }

        self.builder.connect_signals(dic)

    def test(self,widget):
        pass #print 'test'

    def set_passed_filename(self, filepathstring):
        self.fnuri = 'file://'+filepathstring
        #fixing oddity in set_uri, as char % needs to be set as %25 in filepath
        self.fnuri = self.fnuri.replace('%','%25')
        self.builder.get_object('filechooserbutton1').set_uri(self.fnuri)
        print 'recieved passed filename'

    def get_trigger_events_from_data(self,widget):
        print('wid', widget)
        print 't_uri', self.builder.get_object('filechooserbutton1').get_uri()
        print(widget.get_filename())
        try:
            self.p = pdf.read(widget.get_filename())
            self.p.data.setchannels('trig')
            self.p.data.getdata(0, self.p.data.pnts_in_file)
            self.data = self.p.data.data_block
            self.wintime = self.p.data.wintime
            u,n,nz = trigger.vals(self.data)
            event_dict = event_logic.get_ind(u,self.data)
            self.event_tree(None,u,event_dict,treeview='treeview1')
        except TypeError:
            pass

    def set_selected_events_passed(self,widget,data,events,wintime):
        event_dict = {0:events}
        self.event_tree(None,['user sel'],event_dict,treeview='treeview1')
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
        #viewtype.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

    def parse_logic(self,widget):
        #8192>4216,300ms
        liststore,iter = self.View.get_selection().get_selected_rows()
        logic = liststore[iter[0][0]][3]
        trig_vals = logic.split(',')[0].split('>')
        try: timediff = int(logic.split(',')[1].rstrip('ms'))
        except: timediff = 0
        from meg import event_logic

        trig_int = []
        for i in trig_vals: #strings to integers
            trig_int.append(int(i))

        ind_dict = event_logic.get_ind(trig_int,self.data)
        print('indices dict',ind_dict)
        result_ind = event_logic.ind_logic(ind_dict, timediff, self.wintime)
        print(result_ind,'timediff',timediff)

    def plot_events(self,widget):
        plot2dgtk.makewin(self.data.T,self.wintime,plottype='imshow')

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
        liststore = self.builder.get_object("liststore1")
        View = self.builder.get_object("treeview2")

        if self.View.get_columns() == []:
            self.colums_set = True
            self.AddListColumn('Time', 0, View, liststore)
            self.AddListColumn('Event Onset', 1, View, liststore)
            View.set_model(liststore)

    def hideinsteadofdelete(self,widget, ev=None):
        widget.hide()
        return True


if __name__ == "__main__":
    mainwindow = setup_gui()
    mainwindow.window.show()
    fn = '/home/danc/programming/python/data/0611/0611piez/e,rfhp1.0Hz,COH'
    fn = '/home/danc/vault/decrypted/programming/python/data/_data/0611piez/SupinePiez/07%2508%2504@09:33/1/e,rfhp1.0Hz,COH'
    mainwindow.set_passed_filename(fn)
    #fb = mainwindow.builder.get_object('filechooserbutton1')
    #fb.set_uri('file://'+fn)

    #print 'uri', fb.get_uri()
    #print 'uri', fb.get_uri()
    #mainwindow.get_events_from_data(mainwindow.builder.get_object('filechooserbutton1'))
    print('testing')
    gtk.main()
