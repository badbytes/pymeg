#!/usr/bin/python2

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
import sys,os,subprocess
if sys.version >= '3':
    print ('Wrong Python Version. Only Python2 supported.')
    sys.exit(1)
try:
    import pygtk
    pygtk.require("2.0")
except:
    print("PyGTK Version Import Error")
    sys.exit(1)
try:
    import gtk
    import gtk.glade
except:
    print("GTK import error")
    sys.exit(1)
    
#pylab methods
from matplotlib import use;use('GTK')
from matplotlib.figure import Figure
from matplotlib.axes import Subplot
from matplotlib.backends.backend_gtk import show

#load required methods
from pdf2py import pdf, readwrite,lA2array
from numpy import shape, random, sort, array, append, size, arange, ndarray,vstack,mean,zeros
from meg import dipole,plotvtk,plot2dgtk,leadfield,signalspaceprojection,nearest
from mri import img_nibabel as img

#gui modules
from gui.gtk import filter, offset_correct, errordialog, preferences,\
dipoledensity, coregister, timef, data_editor, event_process, parse_instance, \
meg_assistant, errordialog, viewmri, power_spectral_density
from gui.gtk import contour as contour_gtk

#from IPython.Shell import IPShellEmbed
#ipshell = IPShellEmbed()
#ipshell() # this call anywhere in your program will start IPython

class maingui:
    wTree = None 
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("windowTreeview")
        self.statusbar = self.builder.get_object("statusbar")
        self.statusbar_cid = self.statusbar.get_context_id("")
        #self.memorybar = self.builder.get_object("memorybar")
        #self.progressbar = self.builder.get_object("progressbar")
        self.datatree(self)

        dic = {
            "on_menuLoadMEG_activate" : self.fileOpenMEG,
            "on_loadmri_activate" : self.fileOpenMRI,
            "on_loadpythondata_activate" : self.fileOpenPYM,
            "on_loaddipolefile_activate" : self.fileOpenDIP,
            "on_toolbutton1_clicked" : self.testhandler,
            "on_menuQuit_activate" : self.quit,
            "on_filedialogLoad_clicked" : self.fileLoad,
            "on_filedialogCancel_clicked" : self.fileCancel,
            "on_menuAbout_activate" : self.about,
            "on_treeview2_row_activated" : self.treeclicked,
            "on_treebutton1_clicked" : self.treegohome,
            "on_treebutton2_clicked" : self.treeuplevel,
            "on_checkbutton_toggled" : self.meg_assist,
            "on_aboutdialog1_hide" : self.abouthide,
            "on_treebutton3_clicked" : self.treeadd2workspace,
            "on_treeview2_buttonpress" : self.treeclicked,
            "itemselect" : self.itemselect,
            "on_toolbutton4_clicked" : self.add2plot,
            "on_buttonplot_activate" : self.plotdata,
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
            "on_data_editor_clicked" : self.data_editor,
            "on_menu_signal_space_filter_activate" : self.signal_space_filter,
            "on_menu_contour_plot_activate" : self.contour_plot,
            "on_menu_epoch_data_activated" : self.epoch_data,
            "on_power_spectral_density_activate" : self.power_spectral_density,
            "on_test" : self.test,
        }

        self.builder.connect_signals(dic)
        #self.memorystat(self)
        self.parseddatadict = {} #stores path2 loaded data as well as complete data structure
        self.datadict = {} #store the actual loaded data
        self.treelist = [] #appends list with newly clicked items from treeview
        self.treedict = {} #initialize the treeview dictionary.
        #self.queue_store = gtk.ListStore(str)
        self.dataselected = [] #tree item currently selected

        #preference data
        try: self.prefs = readwrite.readdata(os.getenv('HOME')+'/.pymeg.pym')
        except IOError: pass
        self.fill_combo_entries(None)

    def test(self,widget): #dev default function
        print 'tested'
        menu = self.builder.get_object("menufunctions")
        menu.show_all(); menu.hide()
        menu.set_tearoff_state(True)

    def updatestatusbar(self,string): 
        self.statusbar.push(self.statusbar_cid, string)

    def showpopupmenu(self,widget,event):
        print('button ',event.button)
        if event.button == 3:
            m = self.builder.get_object("menufunctions")
            print(widget, event)
            m.show_all()
            m.popup(None,None,None,3,0)

    def data_editor_handler(self,widget):
        self.de = data_editor.setup_gui() #window
        self.de.window.show()

    def hideinsteadofdelete(self,widget, ev=None):
        widget.hide()
        return True

    def showplotwin(self, widget):
        self.builder.get_object('plotdialog').show()

    def abouthide(self,null,null2):
        self.builder.get_object('aboutdialog1').hide()

    def meg_assist(self):
        self.data_assist = meg_assistant.setup(path = self.fn, callback=self.load_megdata_callback)

    def load_megdata_callback(self):
        path = self.data_assist.pdfdata.data.filepath
        self.datadict[path] = self.data_assist.pdfdata
        self.readMEG()

    def loadMRI(self,widget):
        self.builder.get_object("filechooserdialog1").show()
        self.mr = img.read(self.fn)

    def readMEG(self):
        path = self.fn
        self.dataList.clear()
        #convert pdf object to dictonary
        self.parseinstance(self.datadict[path])
        self.refreshdatasummary()

        for i in self.parseddatadict:
            print('appending model', i)
            iter = self.dataList.append([i, self.datadict[path]])

    def refreshdatasummary(self):
        self.parseinstance(self.datadict[self.fn])
        self.datadict[self.fn] = self.parseddata.out
        self.parseddatadict[self.fn] = self.parseddata.out

    def fileOpenMEG(self,widget):
        self.builder.get_object("filechooserdialog1").show()
        self.filetype = '4DMEG'
        self.clear_filters()

    def fileOpenMRI(self,widget):
        fcd = self.builder.get_object("filechooserdialog1")
        filter = gtk.FileFilter()
        filter.set_name("Nifti files")
        filter.add_pattern("*nii.gz")
        filter.add_pattern("*nii")
        self.clear_filters()
        fcd.add_filter(filter)
        fcd.show()
        self.filetype = 'MRI'

    def fileOpenPYM(self,widget):
        fcd = self.builder.get_object("filechooserdialog1")
        filter = gtk.FileFilter()
        filter.set_name("Python")
        filter.add_pattern("*.pym")
        filter.add_pattern("*.pymwf")
        filter.add_pattern("*.pymlf")
        self.clear_filters()
        fcd.add_filter(filter)
        fcd.show()
        self.filetype = 'PYM'

    def fileOpenDIP(self, widget):
        fcd = self.builder.get_object("filechooserdialog1")
        filter = gtk.FileFilter()
        filter.set_name("Dipole Files")
        filter.add_pattern("*lA")
        filter.add_pattern("*.drf")
        self.clear_filters()
        fcd.add_filter(filter)
        fcd.show()
        self.filetype = 'DIP'

    def clear_filters(self):
        fcd = self.builder.get_object("filechooserdialog1")
        for i in fcd.list_filters():
            fcd.remove_filter(i)

    def fileLoad(self,widget):
        self.fn = self.builder.get_object("filechooserdialog1").get_filename()
        self.builder.get_object("filechooserdialog1").hide()
        self.updatestatusbar('loading file'+self.fn)
        if self.parseddatadict.get(self.fn, False) != False:
            errordialog.errorwin('File exists in your workspace. Not reloading.')
            self.updatestatusbar('File exists in your workspace. Not reloading.')
            return

        if self.filetype == '4DMEG':
            print('filetype MEG')
            try:
                pdf.read(self.fn)
                self.meg_assist()
            except AttributeError:
                print('Not a MEG file')

        if self.filetype == 'MRI':
            print('filetype MRI')
            self.datadict[self.fn] = {'nifti':img.loadimage(self.fn)}
            self.refreshdatasummary()
            self.treegohome(None)

        if self.filetype == 'PYM':
            print('filetype PYTHON')
            d = readwrite.readdata(self.fn)
            self.datadict[self.fn] = d
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
        except KeyError:
            readwrite.writedata(self.data_file_selected, fcd.get_filename())
        fcd.hide()

    def quit(self, widget):
        sys.exit(0)

    def memorystat(self,widget): #check and display memory status of machine
        if sys.platform.find('linux') != -1:
            memlist = subprocess.Popen('free',shell=True,stdout=subprocess.PIPE)
            stdout_list=memlist.communicate()[0].split('\n')
            memtotal = stdout_list[1].split()[1]
            memused = stdout_list[1].split()[2]
            mempercent = float(memused)/float(memtotal)
            print('updating memory')
            self.memorybar.set_fraction(mempercent)

    def progressstat(self,widget): #set progress bar value
        self.builder.get_object("label3").set_text(self.progresslabel)
        self.progressbar.set_fraction(1)

    def datatree(self,widget):
        print('updating list')
        self.View = self.builder.get_object("treeview2")
        self.AddListColumn('Variable', 0)
        self.AddListColumn('Data', 1)
        self.dataList = gtk.ListStore(str,str)
        self.View.set_model(self.dataList)

    def AddListColumn(self, title, columnId):
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=columnId)
        column.set_resizable(True)
        column.set_sort_column_id(columnId)
        self.View.append_column(column)

    def parseinstance(self,data):
        self.currentDataName = str(data)
        if self.prefs['VerboseTreeButton'] == True:
            verbose=True
        else:
            verbose=False
        self.parseddata = parse_instance.run(data,verbose)

    def populatetree(self,treedata):
        self.treedata = treedata
        for k in self.treedata.keys():

            if type(self.treedata[k]) == list:# or type(self.treedata[k]) == dict:
                if len(self.treedata[k]) > 50:
                    iter = self.dataList.append([k,'list shape'+str(shape(self.treedata[k]))])
                else:
                    iter = self.dataList.append([k,self.treedata[k]])
            elif type(self.treedata[k]) == ndarray:
                if len(self.treedata[k].flatten()) > 50:
                    iter = self.dataList.append([k,'array shape'+str(shape(self.treedata[k]))])
                else:
                    iter = self.dataList.append([k,self.treedata[k]])
            elif type(self.treedata[k]) == dict:
                iter = self.dataList.append([k,'dict keys'+str(self.treedata[k].keys())])

            else:
                iter = self.dataList.append([k,self.treedata[k]])

    def itemselect(self, widget):
        model,iter = self.builder.get_object("treeview2").get_selection().get_selected()
        print('you selected item:', self.dataList.get_value(iter,0))#, self.dataList.get_value(iter,1)
        self.selecteditem = self.dataList.get_value(iter,0)
        self.dataselected = self.selecteditem

    def treeclicked(self,b,c,d):
        print(b,c,d)
        model,rows = b.get_selection().get_selected()
        iter = self.dataList.get_iter(c[0])
        print('you selected', self.dataList.get_value(iter,0))#, self.dataList.get_value(iter,1))
        self.refreshdatasummary()

        print('you selected position',c[0])
        print('length of tree', len(self.treedict))
        if len(self.treedict) == 0:
            print('at home')
            self.treedata = self.parseddatadict[self.dataList.get_value(iter,0)]
            try: self.treedict[self.treedict.keys()[-1]+1] = self.treedata
            except AttributeError: self.treedict = {0 :self.treedata}
            except IndexError: self.treedict = {0 :self.treedata}
            self.builder.get_object('statusbar').push(self.builder.get_object("statusbar").get_context_id(''),self.dataList.get_value(iter,0))

            self.data_file_selected = self.datadict[self.selecteditem]
            self.data_filename_selected = self.selecteditem
            print('Data File Selected:')#,self.data_file_selected
        else:
            print('lower lvl')
            try: self.treedict[self.treedict.keys()[-1]+1] = self.treedata[self.dataList.get_value(iter,0)]
            except AttributeError: self.treedict = {0 :self.treedata[self.dataList.get_value(iter,0)]}
            self.data2parse = self.treedict[self.treedict.keys()[-1]]
            self.parseinstance(self.data2parse)
            self.treedata = self.parseddata.out

        self.dataList.clear()
        self.populatetree(self.treedata)
        self.builder.get_object('treebutton2').set_sensitive(True)

    def deleteselected(self, widget):
        liststore,iter = self.View.get_selection().get_selected()
        self.selectedvar = self.dataList.get_value(iter,0)
        self.datadict.pop(self.selecteditem)
        self.parseddatadict.pop(self.selecteditem)
        self.treegohome(None)

    def treegohome(self,widget,resave=False):
        print('going home')
        self.treedict = {};
        self.dataList.clear();
        for i in self.parseddatadict:
            iter = self.dataList.append([i,type(self.parseddatadict[i])])#, 'Data File'])
            print('data items...',i)
        self.builder.get_object('treebutton2').set_sensitive(False)

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
        self.dataList.clear()
        print('type of data2parse:', type(self.data2parse))
        if type(self.data2parse) == dict:
            self.treedata = self.data2parse#self.parseddata.out
        else:
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
            c[i].show(); 
            e[i].show();
            e[i].activate();
            col[i].show(); 
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

    def plot2D(self, widget):
        try:
            plot2dgtk.makewin(self.treedata[self.selecteditem],\
            xaxis=arange(size(self.treedata[self.selecteditem],axis=0)))
        except AttributeError:
            print('Plotting Random data')
            plot2dgtk.makewin(random.randn(10))

    def tftplot(self,widget): #using the tft object module tftplot to display imshow.
        if self.checkreq() == -1:
            print('caught error')
            return
        print('wid',widget.get_label())
        self.treedata[self.selecteditem].tftplot(widget.get_label())

    def about(self,widget):
        print('t')
        aboutdialog = self.builder.get_object("aboutdialog1")
        aboutdialog.show()

    def setup_helper(self,var,obj=None):
        '''This function is going to search in two places for a queried variable.
        1st search is below what is selected, or within that instance/dictonary
        2nd search is at the same level as the item selected ie all parents objects.
        ex. var = 'srate';
        if the item instance "data" is selected it will first search within the data object
        and if not found will search at the same level ie all objects in the parent.
        ...
        This is meant to be helper function to find data,
        so it doesn't have to be statically defined all the time.
        '''
        import copy, types, inspect
        #v = [];
        v = {}
        if type(var) == str:
            var = [var] #make list


        for ii in var:
            print('look for dependency',ii)
            if type(obj) == dict:
                print('dict search')
                try:
                    out = obj[ii]
                    print('found as child dict', ii)
                except:
                    try:
                        for i in obj:
                            print('i',i, type(obj[i]))
                            if type(obj[i]) == dict:
                                try:
                                    out = obj[i][ii]
                                    print('found',ii)
                                except: pass

                            if obj[i] == ii:
                                out = obj[i]
                                print('found', i)
                    except:
                        print('cant find instance', ii)

            if isinstance(obj, types.InstanceType):
                print('instance..')
                try:
                    out = eval('obj.'+ii)
                    print('found as child instance', ii)
                except:
                    try:
                        for i in inspect.getmembers(obj):
                            if i[0] == ii:
                                out = i[1]
                                print('found', i[0])
                            if isinstance(i[1], types.InstanceType):
                                for j in inspect.getmembers(i[1]):
                                    if j[0] == ii:
                                        out = j[1]
                                        print('found', j[0])
                    except:
                        print('cant find instance', ii)

            #v.extend([out]);
            v[ii] = out
        if len(v) != len(var):
            print('missing items requested')
            raise KeyError

        return v


    def filter_handler(self,widget):
        def donefilt(results):
            self.data_file_selected['filtered'].data_block = results
        import copy
        self.checkreq()
        self.data_file_selected['filtered'] = copy.copy(self.treedata[self.selecteditem])
        srate = self.setup_helper(var='srate',obj=self.data_file_selected['filtered'])[0]
        self.fil = filter.filtwin()
        print('target',self.target)
        print(shape(self.target))
        try:
            self.fil.setupfilterwin(None, self.target,srate,callback=donefilt)
        except KeyError:
            print('had a prob, bob')
            return -1
        self.fil.builder.get_object('FilterWindow').show()

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
        self.gridwin = grid.gridwin()
        try:
            self.gridwin.mriwin(workspace_data=self.data_file_selected)
        except (AttributeError, KeyError):
            print('no data')
            self.errordialog\
            ('No data selected. Double Click a MEG filename')

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
        self.prefinit = preferences.prefs()
        self.prefinit.window.show()
        self.prefs = self.prefinit.prefs

    def plot2Dmri(self, widget):
        vm = viewmri.setup_gui()
        print(self.treedata[self.selecteditem].data)
        try:
            self.mrimousepos = vm.display(self.treedata[self.selecteditem].data,pixdim=self.treedata[self.selecteditem].pixdim)

        except:# (AttributeError, KeyError):
            try:
                self.mrimousepos = vm.display(self.treedata[self.selecteditem])
                vm.window.show()
            except (AttributeError, KeyError):
                print('Unknown data format')
                self.errordialog('Unknown data format. Try selecting variable = nifti, or data array');

    def plot3DMRIhandle(self, widget):
        from mri import vtkview
        vtkview.show()

    def leadfieldcalc(self, widget):
        if self.checkreq() == -1:
                print('caught error')
                return
        try:
            self.data_file_selected['grid']
        except AttributeError:
            print('grid not detected in results')
            if self.treedata[self.selecteditem] == 'grid':
                print('using selected grid')
            else:
                print('no grid detected. giving up.')
                print('create or load grid first')
                self.gridcalc(None)
                return

        self.lf = leadfield.calc(self.data_file_selected['data'].filename, self.data_file_selected['data'].channels, \
        self.data_file_selected['grid'])
        print('lf shape', self.data_file_selected['grid'].shape)
        print('saving leadfield in workspace')
        self.data_file_selected['leadfield'] = self.lf
        self.data_file_selected['leadfield'].channels = self.data_file_selected['data'].channels
        self.data_file_selected['leadfield'].leadfields_transposed = self.lf.lp.T

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
        def donetft(results):
            self.data_file_selected['tft'] = results
            print(self.data_file_selected['tft'].npoints)
            self.datadict[self.data_filename_selected] = self.data_file_selected
            self.treegohome(None)

        self.tf = timef.setup() #window
        try:
            obj=self.treedata[self.selecteditem];
            res = (self.setup_helper(var=['data_block','labellist','srate','frames',
            'numofepochs','eventtime'],obj=obj));
            print (len(res), 'length')
            self.tf.builder.get_object('filechooserbutton1').set_sensitive(False)
            #self.tf.datahandler(ret[0],ret[1],ret[2][0],ret[3],ret[4][0],ret[5],callback=donetft)
            self.tf.datahandler(res,callback=donetft)
            self.tf.window.show()
            print('tft on data instance')
        except IOError: #tft on data variable selected
            try:

                self.tf.datahandler(self.treedata[self.selecteditem],callback=donetft)
                self.tf.builder.get_object('filechooserbutton1').set_sensitive(False)
                self.tf.builder.get_object('label12').set_text(str(self.selecteditem))
                print ('tft on data variable selected')
                self.tf.window.show()
                print ('tft on data var selected')
            except KeyError:
                self.errordialog\
                ('Unknown data type. Type selecting Variable = data.')
                raise TypeError


    def signal_space_build_weights(self,widget):
        try:
            print ('selection list', self.de.selections)
            self.de.time
            liststore,iter = self.de.SelView.get_selection().get_selected_rows()

        except AttributeError:
            self.errordialog\
            ('No selections made yet. Load file in data editor,\
            and make selections. Then highlight selection with selector tool.')
            raise TypeError


        for i in iter:
            print ('highlighted', liststore[i][1])
            self.de.get_time_selection(widget,current=False)
            print ('indices',self.de.sel_ind)
            data = self.de.data
            self.data_file_selected['signal_projection'] = {}
            self.data_file_selected['signal_projection']['signal_weights'] = data[self.de.sel_ind]

    def signal_space_filter(self,widget):
        
        self.datadict[self.data_filename_selected] = self.data_file_selected
        #sp = self.data_file_selected['signal_projection']
        #obj = self.treedata[self.selecteditem]
        #var = ['channels','srate','numofepochs','labellist',
        #'chanlocs','frames','eventtime','wintime']
        #res = (self.setup_helper(var,obj=obj));
        #data_block = (self.setup_helper(['data_block'],obj=obj))['data_block']
        #ed = self.data_file_selected['epoched_data'] = {}
        #self.result_helper(ed,res)

        if self.signal_space_build_weights(widget) == -1:
            self.data_editor(None)
            return -1
        print ('done!!')
        try:
            sp = self.data_file_selected['signal_projection']
        except KeyError:
            print ("No weights built yet!!")
            self.errordialog("No weights. Select data from data editor and use selector tool to highlight weight. ");
            return -1
        weights = sp['signal_weights']
        try:
            res = self.setup_helper(var='data_block',obj=self.treedata[self.selecteditem])
        except KeyError:
            print ("No appropriate data found!!")
            self.errordialog("Incorrect data selected");
            pass

        ssp = signalspaceprojection.calc(res['data_block'], weight=weights)


        sp['ssp'] = sp['data_block'] = ssp
        var = ['channels','srate','numofepochs','labellist','chanlocs','frames','eventtime','wintime']
        obj = self.treedata[self.selecteditem]
        res = (self.setup_helper(var,obj=obj));
        self.result_helper(sp,res)
        
        #sp['channels'] = {}
        labels = []
        for i in range(0,size(ssp,1)):
            labels.extend(['SigSP'+str(i)])
        sp['labellist'] = labels
        sp['chanlocs'] = \
        array(self.treedata[self.selecteditem].channels.chanlocs[:,0:size(ssp,1)])
        #sp['data_block'] = ssp
        #sp['srate'] = self.treedata[self.selecteditem].srate
        #sp['wintime'] = self.treedata[self.selecteditem].wintime
        #sp['eventtime'] = self.treedata[self.selecteditem].eventtime
        #sp['frames'] = self.treedata[self.selecteditem].frames
        #sp['srate'] = self.treedata[self.selecteditem].srate
        #sp['numofepochs'] = self.treedata[self.selecteditem].numofepochs

    def contour_plot(self,widget):
        try:
            print ('state',self.mc.window.get_property('visible'))
            if self.mc.window.get_property('visible') == False:
                #someone closed the window
                self.mc.window.show()
            print ('done replotting')
        except AttributeError: #first call. setup
            print ('first plot')
            self.mc = contour_gtk.setup_gui()
            self.mc.window.show()

        self.mc.fig.clf()

        chanlocs = self.setup_helper(var='chanlocs',obj=self.treedata['channels'])['chanlocs']
        self.mc.display(self.treedata[self.selecteditem],chanlocs, subplot='on')

    def result_helper(self,newobj,var):
        for i in var.keys():
            newobj[i] = var[i]
        return newobj

    def epoch_data(self,widget):
        def epoch_callback(widget,startcut,endcut):
            self.datadict[self.data_filename_selected] = self.data_file_selected
            obj = self.treedata[self.selecteditem]
            var = ['channels','srate','numofepochs','labellist',
            'chanlocs','frames','eventtime','wintime']
            res = (self.setup_helper(var,obj=obj));
            data_block = (self.setup_helper(['data_block'],obj=obj))['data_block']
            ed = self.data_file_selected['epoched_data'] = {}
            self.result_helper(ed,res)

            print ('cutsize',startcut[0],startcut[1])
            ed['frames'] = endcut[0]-startcut[0]
            ed['eventtime'] = res['eventtime'][startcut[0]:endcut[0]]
            print 'eventtime', len(ed['eventtime'])
            ed['wintime'] = arange(0,res['wintime'][ed['frames']]*len(startcut),res['wintime'][1])
            print ('size of wintime',len(ed['wintime']))

            import time
            ts = time.time()
            print 'Epoching file.'

            tmp_data = zeros((ed['frames'],len(startcut),size(ed['chanlocs'],1)))
            c = 0
            for i,j in zip(startcut,endcut):
                print (shape(tmp_data),shape(data_block[i:j]))
                tmp_data[:,c] = data_block[i:j]
                c = c+1
            print 'widgetname',widget.get_label()
            print 'elapsed time:',time.time()-ts
            avg_data = mean(tmp_data,axis=1)
            tmp_data = tmp_data.reshape((ed['frames']*len(startcut),size(ed['chanlocs'],1)),order='F')


            if widget.get_label() == 'Average':
                print 'Trying to average'
                tmp_data = avg_data;#mean(tmp_data.reshape((ed['frames'],len(startcut),size(ed['chanlocs'],1)),order='F'),axis=1)
                ed['wintime'] = arange(0,res['wintime'][ed['frames']],res['wintime'][1])

            print ('tmpdatashape',shape(tmp_data))

            ed['data_block'] = tmp_data
            self.treegohome(None)

        filepath = self.setup_helper(var='filepath',obj=self.treedata[self.selecteditem])['filepath']
        if os.path.isfile(filepath) == False:
            return -1
        self.ed = event_process.setup_gui()
        self.ed.window.show()
        print ('sending file:'+'file://'+filepath)
        self.ed.set_passed_filename(filepath,callback=epoch_callback)

    def data_editor(self, widget):
        try:
            obj=self.treedata[self.selecteditem];
            r = (self.setup_helper(var=['data_block','srate','wintime',
            'labellist','chanlocs'],obj=obj));
            print (len(r))
            print r.keys()

        except:
            print ("Data Editor can't handle this type")
            print ("Try selecting object <pdf2py.data.read>")
            self.errordialog("Data Editor can't handle this type.Try selecting object <pdf2py.data.read> ");
            return -1

        try:
            self.de = data_editor.setup_gui()
            #self.de.data_handler(r[0],r[1],r[2],r[3],r[4], callback=self.data_editor_callback)
            self.de.data_handler(input_dict=r, callback=self.data_editor_callback)
            self.de.window.show()
        except RuntimeError:
            self.errordialog("Can't do that Dave");

    def data_editor_callback(self):
        print ('Done')
    
    def power_spectral_density(self,widget):
        obj=self.treedata[self.selecteditem];
        res = (self.setup_helper(var=['data_block','srate','labellist','chanlocs'],obj=obj));
        self.psd = power_spectral_density.setup_gui()
        self.psd.datahandler(res)
        self.psd.window.show()
        
        



    def testhandler(self, widget):
        self.prnt(None)
        self.timef_handler(None)

    def testload(self, widget):
        print('clicked')
        fns = ['/home/danc/python/data/0611/0611piez/e,rfhp1.0Hz,COH']

        for i in fns:
            print('i', i)
            self.fn = path = i
            self.datadict[path] = pdf.read(self.fn)
            self.datadict[path].data.setchannels('meg')
            self.datadict[path].data.getdata(0, self.datadict[path].data.pnts_in_file)
            self.chanlist = ['meg']
            self.readMEG()
        #self.datadict[path].results = self.datadict[path].__class__

if __name__ == "__main__":
    mainwindow = maingui()
    mainwindow.window.show()
    mainwindow.testload(None)

    i = 1
    #import code; code.interact(local=locals())
    exit
    gtk.main()

