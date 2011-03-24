#       pymeg.py
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
'''Main GUI Window'''

import pymeg, sys, os, subprocess
from pdf2py import pdf, readwrite,lA2array
from numpy import shape, random, sort, array, append, size, arange, ndarray
from meg import dipole,plotvtk,plot2dgtk,leadfield,signalspaceprojection,nearest
from matplotlib import use
use('GTK')
from matplotlib.figure import Figure
from matplotlib.axes import Subplot
from matplotlib.backends.backend_gtk import show

from gui.gtk import filter, offset_correct, errordialog, preferences,\
dipoledensity, coregister, timef, data_editor, event_process, parse_instance
from gui.gtk import contour as contour_gtk

#from IPython.Shell import IPShellEmbed
#ipshell = IPShellEmbed()
#ipshell() # this call anywhere in your program will start IPython


try:
    import pygtk
    pygtk.require("2.0")
except:
    #print('1'
    pass
try:
    import gtk
    import gtk.glade
except:
    print("GTK Not Availible")
    sys.exit(1)

class maingui:

    wTree = None

#builder = gtk.Builder()
#builder.add_from_file("pymeg.glade")
#window = builder.get_object("window")

    def __init__(self):
        print('sysarg0',sys.argv[0])
        gladepath = os.path.splitext(sys.argv[0])[0]
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladepath+".glade")
        self.window = self.builder.get_object("windowTreeview")
        self.statusbar = self.builder.get_object("statusbar")
        self.statusbar_cid = self.statusbar.get_context_id("test")

        self.memorybar = self.builder.get_object("memorybar")
        self.progressbar = self.builder.get_object("progressbar")
        self.datatree(self)
        self.resulttree(self)
        dic = {
            "on_menuLoadMEG_activate" : self.fileOpenMEG,
            "on_loadmri_activate" : self.fileOpenMRI,
            "on_loadpythondata_activate" : self.fileOpenPYM,
            "on_loaddipolefile_activate" : self.fileOpenDIP,
            "on_toolbutton1_clicked" : self.testhandler, #self.fileOpen,
            "on_menuQuit_activate" : self.quit,
            "on_filedialogLoad_clicked" : self.fileLoad,
            "on_filedialogCancel_clicked" : self.fileCancel,
            "on_menuAbout_activate" : self.about,
            "on_treeview2_row_activated" : self.treeclicked,
            "on_treebutton1_clicked" : self.treegohome,
            "on_treebutton2_clicked" : self.treeuplevel,
            "on_checkbutton_toggled" : self.assistadvance,
            "on_assistant1_apply" : self.readdata,
            "on_aboutdialog1_hide" : self.abouthide,
            "on_treebutton3_clicked" : self.treeadd2workspace,
            "on_treeview2_buttonpress" : self.treeclicked,
            "itemselect" : self.itemselect,
            "on_toolbutton4_clicked" : self.add2plot,
            "on_buttonplot_activate" : self.plotdata,
            "on_Add2Queue_clicked" : self.Add2Queue,
            "on_2Dplot_clicked" : self.plot2D,
            "on_addto3Dplot_clicked" : self.add2plot,
            "gtk_widget_hide" : self.hideinsteadofdelete,
            "on_menufilter_activate" : self.filter_handler,
            "on_menuoffset_activate" : self.offset_handler,
            "on_imagemenuitem6_activate" : self.gridcalc,
            "on_LoadMRI_clicked" : self.loadMRI,
            "on_menuPrefs_activate" : self.loadpreferences,
            "on_2DMRI_activate" : self.plot2Dmri,
            "on_menuleadfield_activate" : self.leadfieldcalc,
            "on_savebutton_clicked" : self.saveselected,
            "on_saveselecteditem_clicked" : self.startsavedialog,
            "on_deletedselecteditem_clicked" : self.deleteselected,
            "on_dipoledensity_activate" : self.dipoledensityhandle,
            "on_coregister_activate" : self.coregister_handler,
            "on_3DMRI_activate" : self.plot3DMRIhandle,
            "showpopupmenu" : self.showpopupmenu ,
            "on_tftplot_activate" : self.tftplot,
            "on_timef_activate" : self.timef_handler ,
            "on_toolbar_data_editor_clicked" : self.data_editor,
            "on_menu_signal_space_filter_activate" : self.signal_space_filter,
            "on_menu_contour_plot_activate" : self.contour_plot,
            "on_menu_epoch_data_activated" : self.epoch_data,
        }

        self.builder.connect_signals(dic)
        #self.memorystat(self)
        self.parseddatadict = {} #stores path2 loaded data as well as complete data structure
        self.datadict = {} #store the actual loaded data
        self.treelist = [] #appends list with newly clicked items from treeview
        self.treedict = {} #initialize the treeview dictionary.
        self.queue_store = gtk.ListStore(str)
        try: self.prefs = readwrite.readdata(os.getenv('HOME')+'/.pymeg.pym')
        except IOError: pass
        self.fill_combo_entries(None)

    def testhandler(self, widget):
        self.prnt(None)
        self.timef_handler(None)

    def updatestatusbar(self,string):
        self.statusbar.push(self.statusbar_cid, string)

    def showpopupmenu(self,widget,event):
        print('button ',event.button)
        if event.button == 3:
            m = self.builder.get_object("menufunctions")
            print(widget, event)
            m.show_all()
            #m.popup(None,None,None,1,0)
            m.popup(None,None,None,3,0)

    def data_editor_handler(self,widget):
        self.de = data_editor.setup_gui() #window
        self.de.window.show()

    def hideinsteadofdelete(self,widget, ev=None):
        widget.hide()
        return True

    def itemselect(self, widget):
        model,iter = self.builder.get_object("treeview2").get_selection().get_selected()
        print('you selected item:', self.dataList.get_value(iter,0))#, self.dataList.get_value(iter,1)
        self.selecteditem = self.dataList.get_value(iter,0)
        self.dataselected = self.selecteditem

    def showplotwin(self, widget):
        self.builder.get_object('plotdialog').show()

    #def testload(self, widget):
        #print('clicked')
        #fns = ['/home/danc/python/data/0611SEF/e,rfhp1.0Hz,n,x,baha001-1SEF,f50lp']#,'/home/danc/python/data/0611piez/SupinePiez/07%08%04@09:33/1/e,rfhp1.0Hz,ra,f50lp,o']
        ##self.builder.get_object("entry1").set_text('it works')
        ##self.statusbar.push(self.statusbar_cid, 'it works')
        #for i in fns:
            #print('i', i)
            #self.fn = path = i
            #self.datadict[path] = pdf.read(self.fn)
            #self.datadict[path].data.setchannels('meg')
            #self.datadict[path].data.getdata(0, self.datadict[path].data.pnts_in_file)
            #self.chanlist = ['meg']
            ##self.builder.get_object("entry2").set_text('0')
            ##self.builder.get_object("entry3").set_text('100')
            #self.readdata(self)

        #self.datadict[path].results = self.datadict[path].__class__

    def abouthide(self,null,null2):
        self.builder.get_object('aboutdialog1').hide()

    def assistadvance(self,widget):#,button):
        self.chanlist = []
        print('something')
        for i in self.builder.get_object('table1'):
            if i.get_active() == True:

                self.chanlist.append(i.get_label())
        if len(self.chanlist) > 0:
            self.assistant.set_page_complete(self.assistant.get_nth_page(1), True)
            self.assistant.set_page_complete(self.assistant.get_nth_page(2), True)
        else:
            self.assistant.set_page_complete(self.assistant.get_nth_page(1), False)
        print(self.chanlist, 'selected')

    def assistMEG(self):
        def dothis():
            print(1)
        self.assistant = self.builder.get_object("assistant1")#.show()
        self.assistant.show()
        self.assistant.set_page_complete(self.assistant.get_nth_page(0), True)
        path = self.fn
        self.datadict[path] = pdf.read(path)
        self.builder.get_object("entry30").set_text(str(self.datadict[path].data.pnts_in_file[0]))

    def readdata(self,widget):
        self.builder.get_object("assistant1").hide()
        path = self.fn
        if self.parseddatadict.get(path, False) != False:
            self.updatestatusbar('File exists in your workspace. Not loading')
            return
        self.dataList.clear()
        self.parseinstance(self.datadict[path])
        datatype = 'meg'
        if datatype == 'meg':
            self.datadict[path] = pdf.read(path)
            self.parseddatadict[path] = self.parseddata.out
            chindex = []
            for c in self.chanlist:
                print('c',c)
                self.datadict[path].data.setchannels(c)
                chindex.extend(self.datadict[path].data.channels.indexlist)

            int(self.builder.get_object("entry30").get_text())
            self.datadict[path].data.getdata(int(self.builder.get_object("entry29").get_text()), \
            int(self.builder.get_object("entry30").get_text()), chindex=chindex)
            try: self.datadict[path].data.channels.getposition()
            except: pass

        self.refreshdatasummary()

        print('datashape', shape(self.datadict[path].data.data_block))

        for i in self.parseddatadict:
            print('appending model', i)
            iter = self.dataList.append([i, self.datadict[path]])

        #make results instance
        self.datadict[path].results = self.datadict[path].__class__

    def refreshdatasummary(self):
        self.parseinstance(self.datadict[self.fn])
        self.parseddatadict[self.fn] = self.parseddata.out
        try:
            self.builder.get_object('label17').set_text(self.datadict[self.fn].data.filename)
            self.builder.get_object('label18').set_text(self.datadict[self.fn].data.filepath)
            self.builder.get_object('label20').set_text(str(1/self.datadict[self.fn].hdr.header_data.sample_period))
        except AttributeError:
            pass
        try:
            self.builder.get_object('label21').set_text(self.datadict[self.fn].filename)
            self.builder.get_object('label23').set_text(self.datadict[self.fn].filename)
        except AttributeError:
            pass

        self.builder.get_object('treebutton3').set_sensitive(True)

    def fileOpenMEG(self,widget):
        self.builder.get_object("filechooserdialog1").show()
        self.filetype = 'MEG'

    def fileOpenMRI(self,widget):
        fcd = self.builder.get_object("filechooserdialog1")
        filter = gtk.FileFilter()
        filter.set_name("Nifti files")
        filter.add_pattern("*nii.gz")
        filter.add_pattern("*nii")
        fcd.add_filter(filter)
        #self.builder.get_object("filechooserdialog1").show()
        fcd.show()
        self.filetype = 'MRI'

    def fileOpenPYM(self,widget):
        fcd = self.builder.get_object("filechooserdialog1")
        filter = gtk.FileFilter()
        filter.set_name("Python")
        filter.add_pattern("*.pym")
        filter.add_pattern("*.pymwf")
        filter.add_pattern("*.pymlf")

        fcd.add_filter(filter)
        fcd.show()
        self.filetype = 'PYM'

    def fileOpenDIP(self, widget):
        fcd = self.builder.get_object("filechooserdialog1")
        filter = gtk.FileFilter()
        filter.set_name("Dipole Files")
        filter.add_pattern("*lA")
        filter.add_pattern("*.drf")
        fcd.add_filter(filter)
        fcd.show()
        self.filetype = 'DIP'


    def fileLoad(self,widget):
        self.fn = self.builder.get_object("filechooserdialog1").get_filename()
        self.builder.get_object("filechooserdialog1").hide()
        self.updatestatusbar('loading file'+self.fn)
        #self.statusbar.push(self.statusbar_cid, 'loading file'+self.fn)

        if self.filetype == 'MEG':
            print('filetype MEG')
            try:
                pdf.read(self.fn)
                self.assistMEG()
            except AttributeError:
                print('Not a MEG file')

        if self.filetype == 'MRI':
            print('filetype MRI')
            from mri import img
            self.datadict[self.fn] = img.read(self.fn)
            self.mr = self.datadict[self.fn] #make a copy for easy use later.
            self.refreshdatasummary()
            self.treegohome(None)

        if self.filetype == 'PYM':
            print('filetype PYM')
            from instantiate import pymeg
            p = pymeg.PYMEG()
            p.data = readwrite.readdata(self.fn)
            #self.datadict[self.fn] = readwrite.readdata(self.fn)
            ##make a nested dict for use in adding results
            #tmp = readwrite.readdata(self.fn)
            #d = {os.path.basename(self.fn): tmp}
            self.datadict[self.fn] = p
            self.refreshdatasummary()
            self.treegohome(None)

        if self.filetype == 'DIP':
            print('filetype Dipole')


            class dipoledata():
                datafile = array([self.fn])
                for i in datafile:
                    print(i)
                    if datafile[0].split(',')[-1] == 'lA': #pdf
                        lA = lA2array.calc(i)
                        lA.points = array([])
                        lA.points = lA.dips[:,1:4] #xyz in meters
                    else:
                        lA = dipole.parsereport(i)
                        lA.points = array([])
                        lA.points = lA.dips[:,1:4]/100 #xyz in meters

                    lA.params = lA.dips

            self.dipoledata = dipoledata()
            self.datadict[self.fn] = self.dipoledata#.dipdict #dipoledata(self)#.dipdict
            self.refreshdatasummary()
            self.treegohome(None)
            print('done')

    def fileCancel(self,widget):
        self.builder.get_object("filechooserdialog1").hide()
        self.builder.get_object("filechooserdialog2").hide()

    def startsavedialog(self,widget):
        self.builder.get_object("filechooserdialog2").show()

    def saveselected(self,widget):
        fcd = self.builder.get_object("filechooserdialog2")

        try:
            readwrite.writedata(self.treedata[self.selecteditem], fcd.get_filename())
        except AttributeError:
            readwrite.writedata(self.datadict[self.selecteditem], fcd.get_filename())
        fcd.hide()

    def quit(self, widget):
        sys.exit(0)

    def memorystat(self,widget):
        if sys.platform.find('linux') != -1:
            memlist = subprocess.Popen('free',shell=True,stdout=subprocess.PIPE)
            stdout_list=memlist.communicate()[0].split('\n')
            memtotal = stdout_list[1].split()[1]
            memused = stdout_list[1].split()[2]
            mempercent = float(memused)/float(memtotal)
            print('updating memory')
            self.memorybar.set_fraction(mempercent)

    def progressstat(self,widget):
        self.builder.get_object("label3").set_text(self.progresslabel)
        self.progressbar.set_fraction(1)

    def datatree(self,widget):
        print('updating list')
        self.View = self.builder.get_object("treeview2")
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
        print('current data string')#,self.currentDataName)
        print 'verbose setting',self.prefs['VerboseTreeButton']
        if self.prefs['VerboseTreeButton'] == True:
            verbose=True
        else:
            verbose=False
        self.parseddata = parse_instance.run(data,verbose)

    def populatetree(self,treedata):
        self.treedata = treedata
        for k in self.treedata.keys():
            if type(self.treedata[k]) != ndarray:
                iter = self.dataList.append([k,self.treedata[k]])
            else:
                if len(self.treedata[k]) > 50:
                    iter = self.dataList.append([k,'array shape'+str(shape(self.treedata[k]))])
                else:
                    iter = self.dataList.append([k,self.treedata[k]])

    def refreshresults(self):
        self.resultList.clear()
        try:
            self.parsedresults = parse_instance.run(self.datadict[self.fn].results)
            for j in self.parsedresults.out.keys():
                iter = self.resultList.append([j,self.parsedresults.out[j]])
        except AttributeError: pass #maybe Nifti

    def treeclicked(self,b,c,d):
        print(b,c,d)
        model,rows = b.get_selection().get_selected()
        iter = self.dataList.get_iter(c[0])
        print('you selected', self.dataList.get_value(iter,0))#, self.dataList.get_value(iter,1))

        self.refreshdatasummary()
        self.refreshresults()

        print('you selected position',c[0])
        print('length of tree', len(self.treedict))
        if len(self.treedict) == 0:
            print('at home')
            self.treedata = self.parseddatadict[self.dataList.get_value(iter,0)]
            try: self.treedict[self.treedict.keys()[-1]+1] = self.treedata
            except AttributeError: self.treedict = {0 :self.treedata}
            except IndexError: self.treedict = {0 :self.treedata}
            self.builder.get_object('statusbar').push(self.builder.get_object("statusbar").get_context_id(''),self.dataList.get_value(iter,0))
            self.builder.get_object('treebutton3').set_sensitive(False)
            self.data_file_selected = self.datadict[self.selecteditem]
            print 'Data File Selected:'#,self.data_file_selected
        else:
            print('lower lvl')
            try: self.treedict[self.treedict.keys()[-1]+1] = self.treedata[self.dataList.get_value(iter,0)]
            except AttributeError: self.treedict = {0 :self.treedata[self.dataList.get_value(iter,0)]}
            self.builder.get_object('treebutton3').set_sensitive(False)
            self.data2parse = self.treedict[self.treedict.keys()[-1]]
            self.parseinstance(self.data2parse)
            self.treedata = self.parseddata.out

        self.dataList.clear()
        self.populatetree(self.treedata)

    def deleteselected(self, widget):
        liststore,iter = self.View.get_selection().get_selected()
        self.selectedvar = self.dataList.get_value(iter,0)
        print self.selectedvar
        self.datadict.pop(self.selecteditem)
        self.parseddatadict.pop(self.selecteditem)
        self.treegohome(None)

    def treegohome(self,widget):
        print('going home')
        self.treedict = {}
        self.dataList.clear()
        for i in self.parseddatadict:
            iter = self.dataList.append([i,type(self.parseddatadict[i])])#, 'Data File'])
            print(i)
        self.builder.get_object('treebutton3').set_sensitive(True)

    def treeuplevel(self,widget):
        print('stepping up a level')
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
        print(self.data2parse,'------------------')
        self.dataList.clear()
        self.parseinstance(self.data2parse)
        self.treedata = self.parseddata.out
        self.populatetree(self.treedata)

    def treeadd2workspace(self,widget):
        liststore,iter = self.View.get_selection().get_selected()
        self.fn = self.dataList.get_value(iter,0)
        print('switching data in workspace to', self.fn)
        path = self.fn
        self.refreshdatasummary()

    def add2plot(self,widget):
        self.builder.get_object('plotdialog').show()

        liststore,iter = self.View.get_selection().get_selected()
        print(iter)
        self.selectedvar = self.dataList.get_value(iter,0)
        try:
            self.plotdict[len(self.plotdict.keys())] = self.treedata[self.selectedvar]
            self.labeldict[len(self.plotdict.keys())] = self.selectedvar
        except AttributeError:
            self.labeldict = {0: self.selectedvar}
            self.plotdict = {0: self.treedata[self.selectedvar]}

        print('labels', self.labeldict)
        c = self.builder.get_object('vbox3').get_children()
        e = self.builder.get_object('vbox5').get_children()
        col = self.builder.get_object('vbox6').get_children()
        shape_type = self.builder.get_object('vbox1').get_children()

        for i in range(0, len(self.labeldict.keys())):
            c[i].set_label(self.labeldict[self.labeldict.keys()[i]])
            c[i].show(); #c[i].set_active(True)
            e[i].show(); e[i].activate()
            col[i].show(); #col[i].activate()
            shape_type[i].show()

    def fill_combo_entries(self,widget):
        shape_type = self.builder.get_object('vbox1').get_children()
        liststore = self.builder.get_object("PlotShape")

        for i in range(0,len(shape_type)):
            cell = gtk.CellRendererText()
            shape_type[i].pack_start(cell)
            shape_type[i].add_attribute(cell, 'text',0)
            shape_type[i].set_model(liststore)
            shape_type[i].set_active(0)

    def plotdata(self,widget): #plot points in 3D
        print('trying to plot in vtk')
        colordict = {}
        sizedict = {}
        self.sel2plot = {}
        plottypedict = {}
        names = self.builder.get_object('vbox3').get_children()
        sizes = self.builder.get_object('vbox5').get_children()
        colors = self.builder.get_object('vbox6').get_children();
        shape_type = self.builder.get_object('vbox1').get_children()
        counternum = 0

        for i in self.builder.get_object('vbox3').get_children():

            if i.get_active() == True:
                print(i), i.get_label()
                self.sel2plot[counternum] = self.plotdict[counternum]
                print(colors[counternum].name)
                r = colors[counternum].get_color().red_float
                g = colors[counternum].get_color().green_float
                b = colors[counternum].get_color().blue_float
                colordict[counternum] = [r,g,b]
                sizedict[counternum] = float(sizes[counternum].get_text())
                if i.get_label() == 'chupos' or i.get_label() == 'chlpos':
                    disk_dir = None
                counternum = counternum + 1
            else: counternum = counternum + 1

        print('colors', colordict)
        print('sizes', sizedict)
        print(self.sel2plot, self.plotdict)
        print('data', self.sel2plot)
        plotvtk.display(self.sel2plot, color = colordict, radius = sizedict)

    def Add2Queue(self, widget):
        try:
            self.queue_store.append([self.selecteditem])
            print('adding',self.selecteditem,'to queue')
        except AttributeError:
            self.queue_store = gtk.ListStore(str)

        self.box.set_active(-1)
        self.box.set_model(self.queue_store)   #this replaces the model set by Glade

        try:
            self.data_queue[self.selecteditem] = self.treedata[self.dataselected]
        except AttributeError:
            self.data_queue = {self.selecteditem : self.treedata[self.dataselected]}

    def plot2D(self, widget):
        try:
            plot2dgtk.makewin(self.treedata[self.selecteditem],\
            xaxis=arange(size(self.treedata[self.selecteditem],axis=0)))
        except AttributeError:
            print('Plotting Random data')
            plot2dgtk.makewin(random.randn(10))

    def tftplot(self,widget):
        if self.checkreq() == -1:
            print('caught error')
            return
        print 'wid',widget.get_label()
        self.treedata[self.selecteditem].tftplot(widget.get_label())

    def loadMRI(self,widget):
        self.builder.get_object("filechooserdialog1").show()
        from mri import img
        self.mr = img.read(self.fn)

    def about(self,widget):
        print('t')
        aboutdialog = self.builder.get_object("aboutdialog1")
        aboutdialog.show()

    def filter_handler(self,widget):
        self.checkreq()
        self.fil = filter.filtwin()#.window.show()
        self.fil.setupfilterwin(None, workspace_data=self.datadict[self.fn], \
        data_selected=self.treedata[self.selecteditem])
        self.updatestatusbar('Data Filtered')

    def offset_handler(self,widget):
        self.checkreq()
        self.offset = offset_correct.offsetwin()#.window.show()
        self.offset.setupoffsetwin(None, workspace_data=self.datadict[self.fn], \
        data_selected=self.treedata[self.selecteditem])

    def gridcalc(self, widget):
        if self.checkreq() == -1:
            print('caught error')
            return

        from gui.gtk import grid
        self.gridwin = grid.gridwin()#.window.show()gridwin
        #self.gridwin.window
        try: self.gridwin.mriwin(workspace_data=self.datadict[self.dataselected])
        except AttributeError:
            print('no data')

    def checkreq(self):
        try: self.fn
        except AttributeError: self.errordialog('No MEG data loaded');self.fileOpenMEG(None);return -1
        try:
            self.selecteditem
        except AttributeError:
            self.errordialog\
            ('No data selected. Select a file from the data explorer')
            return -1

    def errordialog(self, errormesg):
        if self.prefs['ShowErrorDialogButton'] == True:
            error = errordialog.errorwin(errormesg)
        if self.prefs['SpeakErrorButton'] == True:
            from misc import text2speech
            F = text2speech.Festival()
            F.say(errormesg)

    def loadpreferences(self, widget):
        self.prefinit = preferences.prefs()#.prefs.window.show()#.window.show()
        self.prefinit.window.show()
        self.prefs = self.prefinit.prefs

    def plot2Dmri(self, widget):
        from mri import viewmri
        try:
            self.mrimousepos = viewmri.display(self.treedata[self.selecteditem])
        except (AttributeError, KeyError):
            self.mrimousepos = viewmri.display(self.datadict[self.dataselected])

    def plot3DMRIhandle(self, widget):
        from mri import vtkview
        vtkview.show()

    def leadfieldcalc(self, widget):
        if self.checkreq() == -1:
                print('caught error')
                return
        try:
            self.datadict[self.fn].grid
        except AttributeError:
            print('grid not detected in results')
            if self.selecteditem == 'grid':
                print('using selected grid')
            else:
                print('no grid detected. giving up.')
                print('create or load grid first')
                self.gridcalc(None)
                return

        self.lf = leadfield.calc(self.datadict[self.fn], self.datadict[self.fn].data.channels, \
        self.datadict[self.fn].grid)
        print('lf shape', self.datadict[self.fn].grid.shape)
        print('saving leadfield in workspace')
        self.datadict[self.fn].leadfield = self.lf

    def dipoledensityhandle(self,widget):
        self.dd = dipoledensity.density() #window

        try:
            print('dipole shape',shape(self.dipoledata.lA.points))
            self.dd.window.show()
            print('uri',self.dd.builder.get_object('filechooserbutton1').set_uri('file:///'+self.dipoledata.datafile[0]))
        except AttributeError:
            print('need to load file')
            self.errordialog('No Dipole data loaded');self.fileOpenDIP('passfile')#;return
            self.dd.builder.get_object('filechooserbutton1').set_uri(self.dipoledata.datafile[0])
            self.dd.window.show()

    def coregister_handler(self,widget):
        self.cr = coregister.setup() #window
        self.cr.window.show()

    def timef_handler(self,widget):
        self.tf = timef.setup() #window
        try: #tft on data file
            self.tf.builder.get_object('filechooserbutton1').set_uri('file://'+self.selecteditem)
            self.tf.builder.get_object('filechooserbutton1').set_sensitive(False)
            self.tf.datahandler(workspace_data=self.datadict[self.selecteditem])
            print 'tft on data file'
            self.tf.window.show()
        except:
            print 'data error'
        try: #tft on data variable selected
            self.tf.datahandler(workspace_data=self.data_file_selected,data_selected=self.treedata[self.selecteditem])
            self.tf.builder.get_object('filechooserbutton1').set_uri('file://'+self.selecteditem)
            self.tf.builder.get_object('label12').set_text(str(self.selecteditem))

            print 'tft on data variable selected'
            self.tf.window.show()
        except:
            print 'var error'


    def signal_space_build_weights(self,widget):
        try:
            print 'selection list', self.de.selections
            self.de.time
            liststore,iter = self.de.SelView.get_selection().get_selected_rows()
            for i in iter:
                print 'highlighted', liststore[i][1]
                self.de.get_time_selection(widget)
                print 'indices',self.de.sel_ind
                data = self.de.data
                self.data_file_selected.signal_weights = data[self.de.sel_ind]

        except AttributeError:
            self.errordialog\
            ('No selections made yet. Load file in data editor,\
            and make selections. Then highlight selection with selector tool.')
            return -1

    def signal_space_filter(self,widget):
        self.signal_space_build_weights(widget)
        print 'done!!'
        weights = self.data_file_selected.signal_weights
        try:
            data = self.treedata[self.selecteditem]
            print data
        except KeyError:
            data = self.de.data
            pass

        ssp = signalspaceprojection.calc(data, weight=weights)
        self.data_file_selected.ssp = ssp

    def contour_plot(self,widget):
        try:
            print 'state',self.mc.window.get_property('visible')
            if self.mc.window.get_property('visible') == False:
                #someone closed the window
                self.mc.window.show()
            print 'done replotting'
        except AttributeError: #first call. setup
            print 'first plot'
            self.mc = contour_gtk.setup_gui()
            self.mc.window.show()

        self.mc.fig.clf()
        self.mc.display(self.treedata[self.selecteditem],chanlocs = self.data_file_selected.data.channels.chanlocs, subplot='on')

    def epoch_data(self,widget):
        self.ed = event_process.setup_gui()
        self.ed.window.show()
        self.ed.builder.get_object('filechooserbutton1').set_uri('file://'+self.selecteditem)
        self.ed.builder.get_object('filechooserbutton1').set_sensitive(False)
        #self.ed.get_events_from_data(self.ed.builder.get_object('filechooserbutton1'))
        #self.datadict[path].results = self.datadict[path].__class__

    def data_editor(self, widget):
        try:
            data = self.datadict[self.selecteditem].data.data_block
            srate = self.datadict[self.selecteditem].hdr.header_data.sample_period
            wintime = self.datadict[self.selecteditem].data.wintime
            chanlabels = self.datadict[self.selecteditem].data.channels.labellist
            chanlocs = self.datadict[self.selecteditem].data.channels.chanlocs
        except KeyError:
            data = self.treedata[self.selecteditem]
            srate = self.data_file_selected.hdr.header_data.sample_period
            wintime = self.data_file_selected.data.wintime
            chanlabels = arange(0,size(self.treedata[self.selecteditem],1))
            chanlocs = arange(0,size(self.treedata[self.selecteditem],1))

        self.de = data_editor.setup_gui()
        self.de.window.show()
        self.de.data_handler(data,srate,wintime,chanlabels,chanlocs,callback=self.data_editor_callback)


    def data_editor_callback(self):
        print 'Done'


if __name__ == "__main__":
    mainwindow = maingui()
    mainwindow.window.show()
    i = 1
    #import code; code.interact(local=locals())
    exit
    gtk.main()


