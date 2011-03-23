import sys
import subprocess
from gui.gtk import parsepdf
from pdf2py import pdf
from numpy import shape, random

from matplotlib import use
use('GTK')
from matplotlib.figure import Figure  
from matplotlib.axes import Subplot 
from matplotlib.backends.backend_gtk import show  


try:
    import pygtk
    pygtk.require("2.0")
except:
    print '1'
    pass
try:
    import gtk
    import gtk.glade
except:
    print("GTK Not Availible")
    sys.exit(1)

class tst:

    wTree = None

#builder = gtk.Builder()
#builder.add_from_file("gtkproject.glade")
#window = builder.get_object("window")

    def __init__(self):
        self.builder = gtk.Builder()
        #self.builder.add_from_file("gtkproject.glade")
        self.builder.add_from_file("gtkproject.glade")
        self.window = self.builder.get_object("window")
        self.statusbar = self.builder.get_object("statusbar")
        self.statusbar_cid = self.statusbar.get_context_id("test")
        
        self.memorybar = self.builder.get_object("memorybar")
        self.progressbar = self.builder.get_object("progressbar")
        
        #self.builder.get_object('plotdialog').show()
        #self.builder.get_object("treeview2").connect("delete-event", self.hideinsteadofdestroy)
        #self.builder.get_object('FilterWindow').show()
        self.datatree(self)
        self.resulttree(self)
        self.builder.get_object("entry1").set_text('click test button')
        dic = {
            "on_test_clicked" : self.prnt,
            "on_menuLoadMEG_activate" : self.fileOpen,
            "on_toolbutton1_clicked" : self.prnt, #self.fileOpen,
            "on_toolbutton2_toggled" : self.datainfotree,
            "on_menuQuit_activate" : self.quit,
            #"on_quit_clicked" : self.quit,
            "on_filedialogLoad_clicked" : self.fileLoad,
            "on_filedialogCancel_clicked" : self.fileCancel,
            #"on_treeviewcolumn1_clicked" : self.treeclicked,
            "on_menuAbout_activate" : self.about,
            "on_treeview2_row_activated" : self.treeclicked,
            #"on_treeview2_select_cursor_row" : self.treeclicked,
            "on_treebutton1_clicked" : self.treegohome,
            "on_treebutton2_clicked" : self.treeuplevel,
            "on_table1_add" : self.prnt,
            "on_checkbutton_toggled" : self.assistadvance,
            "on_assistant1_apply" : self.readdata,
            "on_aboutdialog1_hide" : self.abouthide,
            "on_treebutton3_clicked" : self.treeadd2workspace,
            "on_treeview2_buttonpress" : self.treeclicked,
            "itemselect" : self.itemselect,
            "on_toolbutton4_clicked" : self.add2plot,
            "on_buttonplot_activate" : self.plotdata,
            "on_menufilter_activate" : self.setupfilterwin,
            "on_updatefiltbox" : self.updatefiltbox,
            "on_Add2Queue_clicked" : self.Add2Queue,
            "startfiltfilt" : self.startfiltfilt,
            "on_2Dplot_clicked" : self.plot2D,
            "on_addto3Dplot_clicked" : self.add2plot,
            "gtk_widget_hide" : self.hideinsteadofdelete,

        }
        #self.wTree.signal_autoconnect( dic )
        #"on_menuplot_activate" : self.showplotwin,
        self.builder.connect_signals(dic)
        #self.prnt(self)
        self.memorystat(self)
        self.parseddatadict = {} #stores path2 loaded data as well as complete data structure
        self.datadict = {} #store the actual loaded data
        self.treelist = [] #appends list with newly clicked items from treeview
        self.treedict = {} #initialize the treeview dictionary.
        #self.assistMEG()
        #self.objects = self.builder.get_objects()
        self.queue_store = gtk.ListStore(str)
        #self.setupfilterwin(self)

    def hideinsteadofdelete(self,widget, ev=None):
        widget.hide()
        return True

    def itemselect(self, widget):
        model,iter = self.builder.get_object("treeview2").get_selection().get_selected()
        print 'you selected', self.dataList.get_value(iter,0)#, self.dataList.get_value(iter,1)
        self.selecteditem = self.dataList.get_value(iter,0)

    def showplotwin(self, widget):
        self.builder.get_object('plotdialog').show()

    def prnt(self, widget):
        print 'clicked'
        fns = ['/home/danc/python/data/0611SEF/e,rfhp1.0Hz,n,x,baha001-1SEF,f50lp']#,'/home/danc/python/data/0611piez/SupinePiez/07%08%04@09:33/1/e,rfhp1.0Hz,ra,f50lp,o']
        self.builder.get_object("entry1").set_text('it works')
        self.statusbar.push(self.statusbar_cid, 'it works')
        #self.memorystat(self)
        #self.builder.get_object("windowTreeview").show()
        for i in fns:
            print 'i', i
            self.fn = path = i
            self.datadict[path] = pdf.read(self.fn)
            self.chanlist = ['meg']
            self.builder.get_object("entry2").set_text('0')
            self.builder.get_object("entry3").set_text('100')
            #data.var = 'meg'
            #self.parseinstance(data)
            #iter = self.dataList.append([data.var, 'test'])
            self.readdata(self)
            #tb = self.builder.get_object("toolbutton2").is_active()

            if self.builder.get_object("toolbutton2").get_active() == True:
                self.builder.get_object("windowTreeview").show()
            else:
                self.builder.get_object("windowTreeview").hide()

    def abouthide(self,null,null2):
        self.builder.get_object('aboutdialog1').hide()


    def assistadvance(self,widget):#,button):
        self.chanlist = []
        for i in self.builder.get_object('table1'):
            if i.get_active() == True:
                #print i.get_label()
                self.chanlist.append(i.get_label())
        if len(self.chanlist) > 0:
            self.assistant.set_page_complete(self.assistant.get_nth_page(0), True)
            self.assistant.set_page_complete(self.assistant.get_nth_page(1), True)
        else:
            self.assistant.set_page_complete(self.assistant.get_nth_page(0), False)
        print self.chanlist, 'selected'

    def assistMEG(self):
        def dothis():
            print 1
        self.assistant = self.builder.get_object("assistant1")#.show()
        self.assistant.show()
        #path = '/home/danc/python/data/0611SEF/e,rfhp1.0Hz,n,x,baha001-1SEF,f50lp'
        path = self.fn
        #self.data = pdf.read(path)
        self.datadict[path] = pdf.read(path)
        self.builder.get_object("entry3").set_text(str(self.datadict[path].data.pnts_in_file[0]))
        #if self.builder.get_object("checkbutton1").get_active() == True: print 'test'


    def readdata(self,widget):
        #self.assistant.destroy()
        #self.parseddatadict = {'meg':'NA','mri':'NA'}
        #path = '/home/danc/python/data/0611SEF/e,rfhp1.0Hz,n,x,baha001-1SEF,f50lp'
        self.builder.get_object("assistant1").hide()
        path = self.fn
        if self.parseddatadict.get(path, False) != False:
            self.statusbar.push(self.statusbar_cid, 'File exists in your workspace. Not loading')
            return
        self.dataList.clear()
        #self.data = pdf.read(path)

        self.parseinstance(self.datadict[path])
        datatype = 'meg'
        if datatype == 'meg':
            #self.data = pdf.read(path)
            self.datadict[path] = pdf.read(path)
            self.parseddatadict[path] = self.parseddata.out
            #self.datadict[path] = self.data #store the actual loaded data
            chindex = []
            for c in self.chanlist:
                print 'c',c
                self.datadict[path].data.setchannels(c)
                #chindex.extend(self.datadict[path].data.channels.channelindexhdr.tolist())
                chindex.extend(self.datadict[path].data.channels.indexlist)
            #print chindex
            #print 'start and end',int(self.builder.get_object("entry2").get_text()), \
            int(self.builder.get_object("entry3").get_text())
            self.datadict[path].data.getdata(int(self.builder.get_object("entry2").get_text()), \
            int(self.builder.get_object("entry3").get_text()), chindex=chindex)

            #from pylab import plot,show
            #plot(self.data.data.data_block);show()
            self.datadict[path].data.channels.getposition()



        self.refreshdatasummary()
        #self.parseinstance(self.datadict[path])
        #self.parseddatadict[path] = self.parseddata.out
        print 'datashape', shape(self.datadict[path].data.data_block)

        for i in self.parseddatadict:
            print 'appending model', i
            iter = self.dataList.append([i, self.datadict[path]])


        #self.treedata = self.parseddata.out

        #make results instance
        self.datadict[path].results = self.datadict[path].__class__



    def refreshdatasummary(self):
        self.parseinstance(self.datadict[self.fn])
        self.parseddatadict[self.fn] = self.parseddata.out
        self.builder.get_object('label17').set_text(self.datadict[self.fn].data.filename)
        self.builder.get_object('label18').set_text(self.datadict[self.fn].data.filepath)
        self.builder.get_object('label20').set_text(str(1/self.datadict[self.fn].hdr.header_data.sample_period))
        self.builder.get_object('treebutton3').set_sensitive(True)


    def datainfotree(self,widget):
        if self.builder.get_object("toolbutton2").get_active() == True:
            self.builder.get_object("windowTreeview").show()
        else:
            self.builder.get_object("windowTreeview").hide()

    def fileOpen(self,widget):
        self.builder.get_object("filechooserdialog1").show()

    def fileLoad(self,widget):
        self.fn = self.builder.get_object("filechooserdialog1").get_filename()
        self.builder.get_object("filechooserdialog1").hide()
        #self.builder.get_object("filelabel").set_label(self.fn.split('/')[-1])
        self.statusbar.push(self.statusbar_cid, 'loading file'+self.fn)
        self.assistMEG()

    def fileCancel(self,widget):
        self.builder.get_object("filechooserdialog1").hide()

    def quit(self, widget):
        sys.exit(0)

    def memorystat(self,widget):
        if sys.platform.find('linux') != -1:
            memlist = subprocess.Popen('free',shell=True,stdout=subprocess.PIPE)
            stdout_list=memlist.communicate()[0].split('\n')
            memtotal = stdout_list[1].split()[1]
            memused = stdout_list[1].split()[2]
            mempercent = float(memused)/float(memtotal)
            print 'updating memory'
            self.memorybar.set_fraction(mempercent)

    def progressstat(self,widget):
        self.builder.get_object("label3").set_text(self.progresslabel)
        self.progressbar.set_fraction(1)
        

    def datatree(self,widget):
        print 'updating list'
        self.View = self.builder.get_object("treeview2")
        self.dataList = gtk.ListStore(str,str)
        #self.dataList.AddListColumn('Variable', 0)
        #self.AddListColumn('Data', 1)
        self.dataList = gtk.ListStore(str,str)
        self.View.set_model(self.dataList)

    def resulttree(self,widget):
        self.View2 = self.builder.get_object("treeview1")

        self.AddListColumn('Variable', 0)
        self.AddListColumn('Data', 1)
        self.resultList = gtk.ListStore(str,str)
        self.View2.set_model(self.resultList)

    def AddListColumn(self, title, columnId):
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=columnId)
        column.set_resizable(True)
        column.set_sort_column_id(columnId)
        self.View.append_column(column)

    def parseinstance(self,data):
        self.currentDataName = str(data)
        print 'current data string',self.currentDataName
        self.parseddata = parsepdf.run(data)

    def populatetree(self,treedata):
        self.treedata = treedata
        for k in self.treedata.keys():
            iter = self.dataList.append([k,self.treedata[k]])
    def refreshresults(self):
        self.resultList.clear()
        self.parsedresults = parsepdf.run(self.datadict[self.fn].results)
        for j in self.parsedresults.out.keys():
            iter = self.resultList.append([j,self.parsedresults.out[j]])


    def treeclicked(self,b,c,d):
        model,rows = b.get_selection().get_selected()
        iter = self.dataList.get_iter(c[0])
        print 'you selected', self.dataList.get_value(iter,0)#, self.dataList.get_value(iter,1)

        print 'you selected position',c[0]
        print 'length of tree', len(self.treedict)
        if len(self.treedict) == 0:

            print 'at home'
            self.treedata = self.parseddatadict[self.dataList.get_value(iter,0)]
            try: self.treedict[self.treedict.keys()[-1]+1] = self.treedata
            except AttributeError: self.treedict = {0 :self.treedata}
            except IndexError: self.treedict = {0 :self.treedata}
            self.builder.get_object('statusbar1').push(self.builder.get_object("statusbar1").get_context_id(''),self.dataList.get_value(iter,0))
            #self.builder.get_object("statusbar1").set_text(self.treedata)
            self.builder.get_object('treebutton3').set_sensitive(False)
        else:
            print 'lower lvl'
            try: self.treedict[self.treedict.keys()[-1]+1] = self.treedata[self.dataList.get_value(iter,0)]
            except AttributeError: self.treedict = {0 :self.treedata[self.dataList.get_value(iter,0)]}
            self.builder.get_object('treebutton3').set_sensitive(False)

            #self.data2parse = self.parseddatafromparseddatadict[self.dataList.get_value(iter,0)]
            self.data2parse = self.treedict[self.treedict.keys()[-1]]
            self.parseinstance(self.data2parse)
            self.treedata = self.parseddata.out

        self.dataList.clear()
        self.populatetree(self.treedata)

    def treegohome(self,widget):
        print 'going home'
        self.treedict = {}
        self.dataList.clear()
        #self.populatetree(self.treedata)
        for i in self.parseddatadict:
            iter = self.dataList.append([i, 'meg'])
            print i
        self.builder.get_object('treebutton3').set_sensitive(True)

    def treeuplevel(self,widget):
        print 'stepping up a level'
        try:
            self.treedict.pop(self.treedict.keys()[-1])
        except IndexError:
            self.treegohome(self)
            return
        self.dataList.clear()
        try:
            self.data2parse = self.treedict[self.treedict.keys()[-1]]
        except IndexError:
            self.treegohome(self)
            return
        self.parseinstance(self.data2parse)
        self.treedata = self.parseddata.out
        self.populatetree(self.treedata)

    def treeadd2workspace(self,widget):
        liststore,iter = self.View.get_selection().get_selected()
        self.fn = self.dataList.get_value(iter,0)
        print 'switching data in workspace to', self.fn
        path = self.fn
        #self.data = self.datadict[fn]
        #print 'shape', self.datadict[path].data.pnts_in_file
        self.refreshdatasummary()

    def add2plot(self,widget):
        self.builder.get_object('plotdialog').show()
        #from pdf2py import readwrite
        liststore,iter = self.View.get_selection().get_selected()
        print iter
        self.selectedvar = self.dataList.get_value(iter,0)
        try:
            self.plotdict[self.selectedvar] = self.treedata[self.selectedvar]
            print shape(self.plotdict[self.selectedvar])
        except AttributeError:
            self.plotdict = {self.selectedvar: self.treedata[self.selectedvar]}
            print shape(self.plotdict[self.selectedvar])
        c = self.builder.get_object('vbox3').get_children()
        e = self.builder.get_object('vbox5').get_children()
        col = self.builder.get_object('vbox6').get_children()

        for i in range(0, len(self.plotdict.keys())):
            c[i].set_label(self.plotdict.keys()[i])
            c[i].show(); c[i].set_active(True)
            e[i].show(); e[i].activate()
            col[i].show(); #col[i].activate()
                    #i.set_label(self.selectedvar)
        #readwrite.writedata(self.plotdict, 'plotdict')

    def plotdata(self,widget):
        print 'trying to plot in vtk'
        colordict = {}
        sizedict = {}
        self.sel2plot = {}
        from meg import plotvtk
        sizes = self.builder.get_object('vbox5').get_children()
        colors = self.builder.get_object('vbox6').get_children();
        counternum = 0

        for i in self.builder.get_object('vbox3').get_children():

            if i.get_active() == True:
                print i
                self.sel2plot[i.get_label()] = self.plotdict[i.get_label()]

        #for i in self.builder.get_object('vbox6').get_children():
            #if i.get_active() == True:
                print colors[counternum].name
                r = colors[counternum].get_color().red_float
                g = colors[counternum].get_color().green_float
                b = colors[counternum].get_color().blue_float
                colordict[counternum] = [r,g,b]


        #for i in self.builder.get_object('vbox5').get_children():
            #if i.get_active() == True:
                sizedict[counternum] = float(sizes[counternum].get_text())
                counternum = counternum + 1

        print 'colors', colordict
        print 'sizes', sizedict
                #var2plot[]
        print self.sel2plot, self.plotdict
        from pdf2py import readwrite
        #readwrite.writedata(self.sel2plot, 'plotdata')
        #readwrite.writedata(colordict, 'colordict')
        #readwrite.writedata(sizedict, 'sizedict')
        plotvtk.display(self.sel2plot, color = colordict, radius = sizedict) #, color=[[255,0,0],[0,255,0]], radius=[[.006],[.006]])

    def Add2Queue(self, widget):
        try:
            self.queue_store.append([self.selecteditem])
            print 'adding',self.selecteditem,'to queue'
        except AttributeError:
            self.queue_store = gtk.ListStore(str)
        self.box.set_active(-1)

        #self.box=self.builder.get_object("combobox1")
        #cell = gtk.CellRendererText()
        #self.box.pack_start(cell, True)
        #self.box.add_attribute(cell, 'text', 0)
        #self.queue_store = gtk.ListStore(str)

        #self.queue_store.append(["Choose a DataSet"])
        self.box.set_model(self.queue_store)   #this replaces the model set by Glade
        #self.box.set_active(0)
        #self.box.show()
        try:
            self.data_queue[self.selecteditem] = self.treedata[self.dataselected]
        except AttributeError:
            self.data_queue = {self.selecteditem : self.treedata[self.dataselected]}

    def setupfilterwin(self, widget):
        print 'filter stuff'
        self.builder.get_object('FilterWindow').show()
        try:
            self.box
            pass
        except AttributeError:

            self.box=self.builder.get_object("combobox1")
            cell = gtk.CellRendererText()
            self.box.pack_start(cell, True)
            self.box.add_attribute(cell, 'text', 0)
            #self.queue_store = gtk.ListStore(str)
            self.queue_store.append(["Choose a DataSet"])
            self.box.set_model(self.queue_store)   #this replaces the model set by Glade
            self.box.set_active(0)
            self.box.show()
        try:
            self.builder.get_object('entry24').set_text(str(1/self.datadict[self.fn].data.hdr.header_data.sample_period[0]))
        except AttributeError:
            pass
        self.updatefiltbox(self)


    def updatefiltbox(self,box):
        #self.box.set_model(self.queue_store)
        #self.model = box.get_model()
        #self.index = box.get_active()
        #if self.index:
            #print  self.model[self.index][0], 'selected'
            #self.dataselected = self.model[self.index][0]
            
        for i in self.builder.get_object("hbox7"):
            if i.get_active() == True:
                self.band = i.get_label()
        if self.band == 'low':
            self.Wn = [float(self.builder.get_object('entry25').get_text())]
            self.builder.get_object('entry26').set_sensitive(False);self.builder.get_object('entry25').set_sensitive(True)
        elif self.band == 'high':
            self.Wn = [float(self.builder.get_object('entry26').get_text())]
            self.builder.get_object('entry25').set_sensitive(False);self.builder.get_object('entry26').set_sensitive(True)
        else:
            self.builder.get_object('entry26').set_sensitive(True);self.builder.get_object('entry25').set_sensitive(True)
            self.Wn = [float(self.builder.get_object('entry25').get_text()), float(self.builder.get_object('entry26').get_text())]

    def startfiltfilt(self,widget):
        from meg import filtfilt

        print 'dt',self.treedata[self.selecteditem]#self.dataselected]
        data = self.treedata[self.selecteditem]#self.dataselected] #eval('self.datadict[self.fn].'+self.dataselected)
        #data = self.data_queue[self.selecteditem]
        srate = float(self.builder.get_object('entry24').get_text())
        
        #Wn = [float(self.builder.get_object('entry25').get_text()), float(self.builder.get_object('entry26').get_text())]
            
        order = int(self.builder.get_object('entry27').get_text())
        
         #self.builder.get_object("radiobutton1")
        #print self.treedata[self.dataselected], srate,Wn,order, band#, self.treedata
        #return
        self.datadict[self.fn].results.fil = filtfilt.calc(data, srate, self.Wn, order, self.band)
        self.refreshdatasummary()
        self.refreshresults()
        print shape(self.datadict[self.fn].results.fil)
        self.progresslabel = 'filter'; self.progressstat(None)
        
    def plot2D(self, widget):
        from meg import plot2dgtk
        try:
            plot2dgtk.makewin(self.treedata[self.selecteditem])
        except AttributeError:
            plot2dgtk.makewin(random.randn(10))
        #data = random.randn(10)
        
        
        #plot2dgtk.makewin(data)
        

    def about(self,widget):
        print 't'
        aboutdialog = self.builder.get_object("aboutdialog1")
        aboutdialog.show()


#letsdothis = tst()

if __name__ == "__main__":
    mainwindow = tst()
    mainwindow.window.show()
    gtk.main()
    #a = about()
    #a.window.show()
