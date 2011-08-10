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
import sys,os,subprocess,time,gobject
import threading
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
print '1'
from gui.gtk import errordialog
try:
    from numpy import *
    from scipy import io
except ImportError:
    errordialog.errorwin('Numerical libraries missing. Install Numpy and Scipy. Exiting!')
    sys.exit()
print '2'
try:
    import nibabel
except ImportError:
    errordialog.errorwin('MRI module Nibabel missing, MRI tools will not function properly.')
    sys.exit()

#pylab methods
try:
    from matplotlib import use;use('GTK')
    from matplotlib.figure import Figure
    from matplotlib.axes import Subplot
    from matplotlib.backends.backend_gtk import show
except ImportError:
    errordialog.errorwin('Matplotlib missing. Plotting tools will not work properly')
    sys.exit()
print '3'
#gui modules
try:
    from gui.gtk import filter, offset_correct, errordialog, preferences,\
    dipoledensity, coregister, timef, data_editor, event_process, parse_instance, \
    meg_assistant, errordialog, viewmri, power_spectral_density, progressbar, spinner, filechooser, \
    ica

    from gui.gtk import contour as contour_gtk

except ImportError:
    errordialog.errorwin('PyMEG not installed correctly, cant find pymeg code in path.')
    #sys.exit()
print '4'
#load required methods
try:
    from pdf2py import pdf, readwrite,lA2array
    from meg import dipole,plotvtk,plot2dgtk,signalspaceprojection,nearest
    from meg import leadfield_parallel as leadfield
    from mri import img_nibabel as img
    from mri import sourcesolution2img
    from beamformers import minimumnorm
except ImportError:
    errordialog.errorwin('PyMEG not installed correctly, cant find pymeg code in path.')
    #sys.exit()

print '5'
#from IPython.Shell import IPShellEmbed
#ipshell = IPShellEmbed()
#ipshell() # this call anywhere in your program will start IPython

class maingui():
    wTree = None
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("windowTreeview")
        self.window.show()
        self.statusbar = self.builder.get_object("statusbar")
        self.statusbar_cid = self.statusbar.get_context_id("")
        #self.memorybar = self.builder.get_object("memorybar")
        #self.progressbar = self.builder.get_object("progressbar")
        #self.progressbar = progressbar.setup()

        self.datatree(self)

        dic = {
            "on_loadmeg_activate" : self.fileOpenMEG,
            "on_loadmri_activate" : self.fileOpenMRI,
            "on_loadpythondata_activate" : self.fileOpenPYM,
            "on_loaddipolefile_activate" : self.fileOpenDIP,
            "on_loadmatlabdata_activate" : self.fileOpenMAT,
            "on_toolbutton1_clicked" : self.testhandler,
            "on_menuQuit_activate" : self.quit,
            "on_filedialogLoad_clicked" : self.fileLoad,
            "on_filedialogCancel_clicked" : self.fileCancel,
            "on_menuAbout_activate" : self.about,
            "on_row_activated" : self.treeclicked,
            "on_treebutton1_clicked" : self.treegohome,
            "on_treebutton2_clicked" : self.treeuplevel,
            "on_checkbutton_toggled" : self.meg_assist,
            "on_aboutdialog1_hide" : self.abouthide,
            "on_treebutton3_clicked" : self.treeadd2workspace,
            "on_treeview2_buttonpress" : self.treeclicked,
            "on_selection" : self.itemselect,
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
            "on_saveselecteditem_clicked" : self.savedialog,
            "on_deletedselecteditem_clicked" : self.deleteselected,
            "on_dipoledensity_activate" : self.dipoledensityhandle,
            "on_coregister_activate" : self.coregister_handler,
            "on_3DMRI_activate" : self.plot3DMRIhandle,
            "on_button_press_event" : self.button_press_event ,
            "on_tftplot_activate" : self.tftplot,
            "on_timef_activate" : self.timef_handler,
            "on_data_editor_clicked" : self.data_editor,
            "on_menu_signal_space_filter_activate" : self.signal_space_filter,
            "on_menu_contour_plot_activate" : self.contour_plot,
            "on_menu_epoch_data_activated" : self.epoch_data,
            "on_power_spectral_density_activate" : self.power_spectral_density,
            "on_minimumnorm_activate" : self.minimunnorm_handler,
            "on_solution_to_image_activate" : self.sourcesolution2img_handler,
            "on_function_menu_clicked" : self.menu_tearoff,
            "on_key_press_event" : self.key_press_event,
            "on_copy_activate" : self.copy_item,
            "on_paste_activate" : self.paste_item,
            "on_rename_activate" : self.rename_item,
            "on_closefile_clicked" : self.close_file,
            "on_write_changes_activate" : self.update_changes_meg,
            "on_message_dialog_response" : self.message_dialog_response,
            "on_message_dialog_cancel_clicked" : self.message_dialog_response,
            "on_ica_activate" : self.independent_component_analysis,
        }

        self.builder.connect_signals(dic)
        self.parseddatadict = {} #stores path2 loaded data as well as complete data structure
        self.datadict = {} #store the actual loaded data
        self.treelist = [] #appends list with newly clicked items from treeview
        self.treedict = {} #initialize the treeview dictionary.
        self.dataselected = [] #tree item currently selected
        self.data_filename_selected = [] #filename/path of loaded file

        #turn off function menu and file save menu
        menufunctions = self.builder.get_object('menufunctions').get_children()
        for m in menufunctions:
            if m.get_name() ==  'GtkMenuItem':
                m.set_sensitive(False)
        self.builder.get_object('savefile').set_sensitive(False)
        #self.builder.get_object('updatefile_4D').set_sensitive(False)

        #preference data
        try:
            self.prefs = readwrite.readdata(os.getenv('HOME')+'/.pymeg.pym')
        except IOError:
            self.prefs = {'VerboseTreeButton' : False};
            readwrite.writedata(self.prefs, os.getenv('HOME')+'/.pymeg')
        self.fill_combo_entries(None)

    def menu_tearoff(self,widget): #dev default function
        print 'tested'
        menu = self.builder.get_object("menufunctions")
        menu.show_all(); menu.hide()
        menu.set_tearoff_state(True)

    def updatestatusbar(self,string):
        self.statusbar.push(self.statusbar_cid, string)

    def progresspulse(self):
        p = progressbar.MainThread()
        p.main(testfunction)

    def button_press_event(self,widget,event):
        try:
            print('button ',event)#.button)
            if event.button == 3:
                m = self.builder.get_object("menufunctions")
                print(widget, event)
                m.show_all()
                m.popup(None,None,None,3,0)
            if event.button == 1:
                print 'trying to select'
                #self.itemselect(None)
        except:
            print 'error with mouse click'

    def copy_item(self, widget):
        print self.dataselected, 'copied item to clipboard'
        self.clipboarddata = self.treedata[self.selecteditem]
        self.clipboarditem = self.selecteditem

    def paste_item(self, widget):
        print 'pasting item',self.dataselected
        self.treedata[self.clipboarditem] = self.clipboarddata
        self.refreshtree()

    def key_press_event(self,widget,event):
        if event.keyval == 99:# or widget.get_label() == 'Copy':# and len(event.string) == 0:
            self.copy_item(None)
        if event.keyval == 118:# or widget.get_label() == 'Paste':# and len(event.string) == 0:
            self.paste_item(None)

    def rename_item(self,widget):
        print 'renaming', self.selecteditem
        print widget.get_label()
        if widget.get_label() == 'Rename':
            self.rename_win = self.builder.get_object('rename_dialog')
            self.rename_win.show()
        if widget.get_label() == 'Save':
            print 'renaming item'
            entryfield = self.builder.get_object('rename_entry')
            newname = str(entryfield.get_text())
            self.treedata[newname] = self.treedata[self.selecteditem]
            self.treedata.pop(self.selecteditem)
            self.rename_win.hide()
            self.refreshtree()
        if widget.get_label() == 'Cancel':
            print 'canceling'
            self.rename_win.hide()

    def close_file(self, widget):
        self.datadict.pop(self.data_filename_selected)
        self.parseddatadict.pop(self.data_filename_selected)
        self.treegohome(self)

    def hideinsteadofdelete(self,widget, ev=None):
        widget.hide()
        return True

    def showplotwin(self, widget):
        self.builder.get_object('plotdialog').show()

    def abouthide(self,null,null2):
        self.builder.get_object('aboutdialog1').hide()

    def meg_assist(self):
        self.data_assist = meg_assistant.setup(path = self.fn, callback=self.load_megdata_callback)

    def load_megdata_callback(self,widget=None):
        path = self.data_assist.pdfdata.data.filepath
        self.datadict[path] = self.data_assist.pdfdata
        self.readMEG()
        self.builder.get_object('updatefile_4D').set_sensitive(True)

    def loadMRI(self,widget):
        self.builder.get_object("filechooserdialog").show()
        self.mr = img.read(self.fn)

    def readMEG(self):
        path = self.fn
        self.dataList.clear()
        #convert pdf object to dictonary
        self.parseinstance(self.datadict[path])
        self.refreshdatasummary()

        for i in self.parseddatadict:
            print('appending model', i)
            iter = self.dataList.append([i, self.datadict[path]])#,True])

    def refreshdatasummary(self):
        self.parseinstance(self.datadict[self.fn])
        self.datadict[self.fn] = self.parseddata.out
        self.parseddatadict[self.fn] = self.parseddata.out

    def fileOpenMEG(self,widget):
        fcd = self.builder.get_object("filechooserdialog")
        fcd.show()
        try: fcd.set_current_folder(self.prefs['LastMEGPath'])
        except: pass
        self.filetype = '4DMEG'
        self.clear_filters()

    def fileOpenMRI(self,widget):
        fcd = self.builder.get_object("filechooserdialog")
        filter = gtk.FileFilter()
        filter.set_name("MRI Nifti or Analyze files")
        filter.add_pattern("*nii.gz")
        filter.add_pattern("*nii")
        filter.add_pattern("*img")
        self.clear_filters()
        fcd.add_filter(filter)
        try:fcd.set_current_folder(self.prefs['LastMRIPath'])
        except: pass

        fcd.show()
        self.filetype = 'MRI'

    def fileOpenPYM(self,widget):
        fcd = self.builder.get_object("filechooserdialog")
        filter = gtk.FileFilter()
        filter.set_name("Python")
        filter.add_pattern("*.pym")
        filter.add_pattern("*.pymwf")
        filter.add_pattern("*.pymlf")
        self.clear_filters()
        fcd.add_filter(filter)
        try:fcd.set_current_folder(self.prefs['LastPYMPath'])
        except: pass
        fcd.show()
        self.filetype = 'PYM'

    def fileOpenDIP(self, widget):
        fcd = self.builder.get_object("filechooserdialog")
        filter = gtk.FileFilter()
        filter.set_name("Dipole Files")
        filter.add_pattern("*lA")
        filter.add_pattern("*.drf")
        self.clear_filters()
        fcd.add_filter(filter)
        try:fcd.set_current_folder(self.prefs['LastDIPPath'])
        except: pass
        fcd.show()
        self.filetype = 'DIP'

    def fileOpenMAT(self, widget):
        fcd = self.builder.get_object("filechooserdialog")
        filter = gtk.FileFilter()
        filter.set_name("Matlab Files")
        filter.add_pattern("*.mat")
        #filter.add_pattern("*.set")
        self.clear_filters()
        fcd.add_filter(filter)
        try:fcd.set_current_folder(self.prefs['LastMATPath'])
        except: pass
        fcd.show()
        self.filetype = 'MAT'

    def clear_filters(self):
        fcd = self.builder.get_object("filechooserdialog")
        for i in fcd.list_filters():
            fcd.remove_filter(i)

    def fileLoad(self,widget):
        self.fn = self.builder.get_object("filechooserdialog").get_filename()
        print 'trying to load', self.fn
        pathtofile = os.path.dirname(self.fn)
        self.builder.get_object("filechooserdialog").hide()
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
                self.prefs['LastMEGPath'] = self.fn#pathtofile
                readwrite.writedata(self.prefs, os.getenv('HOME')+'/.pymeg')

            except AttributeError:
                print('Not a MEG file')

        if self.filetype == 'MRI':
            print('filetype MRI')
            self.datadict[self.fn] = {'mri':img.loadimage(self.fn)}
            self.prefs['LastMRIPath'] = pathtofile
            readwrite.writedata(self.prefs, os.getenv('HOME')+'/.pymeg')
            self.refreshdatasummary()
            self.treegohome(None)

        if self.filetype == 'PYM':
            print('filetype PYTHON')
            d = readwrite.readdata(self.fn)
            self.datadict[self.fn] = d
            self.prefs['LastPYMPath'] = pathtofile
            readwrite.writedata(self.prefs, os.getenv('HOME')+'/.pymeg')
            self.refreshdatasummary()
            self.treegohome(None)

        if self.filetype == 'MAT':
            print('filetype MATLAB')
            d = io.loadmat(self.fn)
            self.datadict[self.fn] = d
            self.refreshdatasummary()
            self.prefs['LastMATPath'] = pathtofile
            readwrite.writedata(self.prefs, os.getenv('HOME')+'/.pymeg')
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
        self.builder.get_object('savefile').set_sensitive(True)
        print('done')

    def fileCancel(self,widget):
        self.builder.get_object("filechooserdialog").hide()
        self.builder.get_object("filesavedialog").hide()

    def savedialog(self,widget):
        self.builder.get_object("filesavedialog").show()

    def saveselected(self,widget):
        fcd = self.builder.get_object("filesavedialog")
        filename_without_ext = fnstrip = os.path.splitext(fcd.get_filename())[0]
        try:
            readwrite.writedata(self.treedata[self.selecteditem], fnstrip)
        except AttributeError:
            readwrite.writedata(self.datadict[self.selecteditem], fnstrip)
        except KeyError:
            readwrite.writedata(self.data_file_selected, fnstrip)
        fcd.hide()

    def update_changes_meg(self,widget):
        self.builder.get_object('messagedialog').set_markup('You are saving object '+self.selecteditem+' to file. Do you want to make a copy of the original file as a backup?')
        #print 'is active',self.builder.get_object('messagedialog').is_active()
        #self.builder.get_object('messagedialog').add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE)
        self.builder.get_object('messagedialog').show()
        print 'Using',self.selecteditem,'for the rewrite'

    def message_dialog_response(self,widget,button=False):
        print button

        if button == -8: #OK
            #m = self.builder.get_object('messagedialog')
            #m(parent=None, flags=0, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_NONE, message_format=None)

            try:
                self.builder.get_object('messagedialog-action_area').set_sensitive(False)
                self.spin('start')
                import shutil
                print self.data_filename_selected,'sel'
                shutil.copy(self.data_filename_selected, self.data_filename_selected + '.backup')
                print 'Copy complete to file', self.data_filename_selected + '.backup'
                pdf.write_changes(self.data_file_selected['data'], self.treedata[self.selecteditem])
                print self.treedata[self.selecteditem], 'changes saved to file:',self.data_filename_selected
                self.updatestatusbar('changes saved')
                self.builder.get_object('messagedialog-action_area').set_sensitive(True)
                self.builder.get_object('messagedialog').hide()
            except IOError:
                print 'Error in copy'
                self.updatestatusbar('Error in copy')
                self.builder.get_object('messagedialog-action_area').set_sensitive(True)


        if button == -9: #No backup copy, but still proceed with save.
            self.spin('start')
            pdf.write_changes(self.data_file_selected['data'], self.treedata[self.selecteditem])
            self.builder.get_object('messagedialog').hide()
            self.updatestatusbar('changes saved for file:'+self.data_filename_selected)

        if button == 0: #Cancel
            self.builder.get_object('messagedialog').hide()

        self.spin('stop')

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
        #self.AddListColumn('Data', True)
        self.dataList = gtk.ListStore(str,str)
        self.View.set_model(self.dataList)

    def AddListColumn(self, title, columnId):
        def cell_edited_callback():
            print 'editing'
        cell = gtk.CellRendererText()
        cell.connect('edited', cell_edited_callback)
        cell.set_property('editable', True)
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=columnId)#, editable=2)#, active=0,activatable=0)
        column.set_resizable(True)
        column.set_sort_column_id(columnId)
        self.View.append_column(column)

    def parseinstance(self,data):
        self.currentDataName = str(data)
        try:
            if self.prefs['VerboseTreeButton'] == True:
                verbose=True
            else:
                verbose=False
        except IOError:
            pass
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
        self.dataselected = self.selecteditem = self.dataList.get_value(iter,0)
        self.prerequisite(itemtype='selecteditem')
        if len(self.treedict) == 0:
            self.data_filename_selected = self.selecteditem
            self.data_file_selected = self.datadict[self.selecteditem]

    def treeclicked(self,b,c,d):
        print(b,c,d)
        model,rows = b.get_selection().get_selected()
        iter = self.dataList.get_iter(c[0])
        print('you selected', self.dataList.get_value(iter,0))#, self.dataList.get_value(iter,1))
        #self.refreshdatasummary()

        print('you selected position',c[0])
        print('length of tree', len(self.treedict))
        if len(self.treedict) == 0:
            print('at home')
            self.treedata = self.parseddatadict[self.dataList.get_value(iter,0)]
            try: self.treedict[self.treedict.keys()[-1]+1] = self.treedata
            except AttributeError: self.treedict = {0 :self.treedata}
            except IndexError: self.treedict = {0 :self.treedata}
            self.builder.get_object('statusbar').push(self.builder.get_object("statusbar").get_context_id(''),self.dataList.get_value(iter,0))

            #self.data_file_selected = self.datadict[self.selecteditem]
            #self.data_filename_selected = self.selecteditem
            print('Data File Selected:')#,self.data_file_selected
        else:
            print('lower lvl')
            try: self.treedict[self.treedict.keys()[-1]+1] = self.treedata[self.dataList.get_value(iter,0)]
            except AttributeError: self.treedict = {0 :self.treedata[self.dataList.get_value(iter,0)]}
            self.data2parse = self.treedict[self.treedict.keys()[-1]]
            self.parseinstance(self.data2parse)
            self.treedata = self.parseddata.out
        print 'current level in tree:',self.treedict.keys()

        self.refreshtree()
        self.builder.get_object('treebutton2').set_sensitive(True)

    def deleteselected(self, widget):
        liststore,iter = self.View.get_selection().get_selected()
        self.selectedvar = self.dataList.get_value(iter,0)
        print 'deleting', self.selecteditem
        try:
            #delete whole dataset
            self.datadict.pop(self.selecteditem)
            self.parseddatadict.pop(self.selecteditem)
            self.treegohome(self)
        except KeyError:
            #delete item
            self.treedata.pop(self.selecteditem)
            self.refreshtree()

    def refreshtree(self):
        print 'len',len(self.treedict.keys())
        if len(self.treedict.keys()) > 1: #bug in delete item. cant seem to delete higher than 2 dictionary items.
            self.builder.get_object('deleteselecteditem').set_sensitive(False)
        else:
            self.builder.get_object('deleteselecteditem').set_sensitive(True)
        self.dataList.clear()
        print 'level',self.treedict.keys()
        self.populatetree(self.treedata)
        self.datadict[self.data_filename_selected] = self.data_file_selected
        self.prerequisite(itemtype='generalitem')

    def treegohome(self,widget,resave=False):
        print('going home')
        self.treedict = {};
        self.dataList.clear();
        for i in self.parseddatadict:
            iter = self.dataList.append([i,type(self.parseddatadict[i])])#, 'Data File'])
            print('data items...',i)
        self.builder.get_object('treebutton2').set_sensitive(False)
        self.prerequisite(itemtype='generalitem')

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

        self.refreshtree()

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
        D = self.treedata[self.selecteditem]
        try:
            if shape(D)[0] == 3 and shape(D)[0] != 3:
                D = D.T
            plot2dgtk.makewin(D, xaxis=arange(size(D,axis=0)))
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

    def setup_helper(self,var,obj=None,par=None):
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

        def instance_search(item):
            try:
                #print 'looking for child'
                out = eval('item.'+ii)
            except:
                try:
                    for i in inspect.getmembers(item):
                        if i[0] == ii:
                            out = i[1]
                        if isinstance(i[1], types.InstanceType):
                            for j in inspect.getmembers(i[1]):
                                if j[0] == ii:
                                    out = j[1]
                except:
                    pass
            return out
        def dict_search(item):
            try:
                out = item[ii]
            except:
                try:
                    for i in item:
                        if type(item[i]) == dict:
                            try:
                                out = item[i][ii]
                            except: pass
                        if obj[i] == ii:
                            out = item[i]
                        if isinstance(item[i], types.InstanceType):
                            try: out = instance_search(item[i])
                            except: pass
                except:
                    pass
            return out

        for ii in var:
            if type(obj) == dict:
                try:
                    v[ii] = dict_search(obj)
                except UnboundLocalError:
                    pass

            if isinstance(obj, types.InstanceType):
                try:
                    v[ii] = instance_search(obj)
                except UnboundLocalError:
                    pass

        if len(v) != len(var):
            raise KeyError

        return v

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
        try:
            self.vm.fig.clf()
            #if self.vm.window.get_property('visible') == False:
            #    self.vm.window.show()
        except AttributeError, NameError:
            self.vm = viewmri.setup_gui()
            #self.vm.window.show()

        obj=self.treedata#[self.selecteditem];
        try:
            if self.treedata[self.selecteditem].__module__.split('.')[0] == 'mri':
                print('displaying default MR: data')
                obj=self.treedata[self.selecteditem];
                res = (self.setup_helper(var=['pixdim','data','translation'],obj=obj));
                self.mrimousepos = self.vm.display(data=squeeze(res['data']),pixdim=res['pixdim'],translation=res['translation'])
        except AttributeError:
            print('displaying custom data:',self.selecteditem)
            #obj=self.treedata;
            #res = (self.setup_helper(var=['data'],obj=obj));
            data = self.treedata[self.selecteditem];
            self.mrimousepos = self.vm.display(data,pixdim=[1,1,1],translation=[0,0,0])#squeeze(res['data']))
        self.vm.window.show()

    def plot3DMRIhandle(self, widget):
        from mri import vtkview
        vtkview.show()

    def gridcalc(self, widget):
        def setgrid(grid,mr=None):
            self.data_file_selected['grid'] = grid #in mm
            if mr != None:
                self.data_file_selected['source_space'] = {'pixdim':mr.pixdim*mr.factor,'data':mr.img,'ind':mr.ind,'megxyz':mr.megxyz,'data':mr.data,'img':mr.img} #in mm
            gridwin.window.hide()
            self.updatestatusbar('grid calculation of '+str(size(grid,1))+' points complete')
            self.refreshtree()

        if self.checkreq() == -1:
            print('caught error')
            return

        from gui.gtk import grid
        gridwin = grid.gridwin()
        obj=self.treedata#[self.selecteditem];
        res = (self.setup_helper(var=['hs'],obj=obj));
        gridwin.headshape = res['hs']
        gridwin.builder.get_object("filechooserbutton2").set_sensitive(False)
        gridwin.datahandler(setgrid)
        gridwin.window.show()# = grid.gridwin()


    def leadfieldcalc(self, widget):
        def leadfieldthread():
            if self.checkreq() == -1:
                    print('caught error')
                    return

            obj=self.treedata;#[self.selecteditem];
            res = (self.setup_helper(var=['channels','grid'],obj=obj));
            print 'grid print',res['grid']

            try:
                self.data_file_selected['grid']
            except(AttributeError,KeyError):
                print('grid not detected')
                self.errordialog('No grid detected');
                return -1

                if self.treedata[self.selecteditem] == 'grid':
                    print('using selected grid')
                else:
                    print('no grid detected. giving up.')
                    print('create or load grid first')
                    self.gridcalc(None)
                    return
            self.lf = leadfield.calc(res['channels'],self.data_file_selected['grid'])
            self.data_file_selected['leadfield'] = self.lf
            print type(self.lf)
            self.data_file_selected['leadfield'].channels = res['channels']
            self.refreshtree()
            self.updatestatusbar('leadfield calculation complete')

        MT = progressbar.MainThread()
        MT.main(leadfieldthread)

    def minimunnorm_handler(self,widget):
        def minnormthread():
            obj=self.treedata;
            res = (self.setup_helper(var=['selection_event','leadfield','selection_noise','channels'],obj=obj));
            noisecov = dot(res['selection_noise'].T,res['selection_noise'])
            minnormpow,w = minimumnorm.calc(res['selection_event'],res['leadfield'],noisecov)
            print 'Min Norm Done'

            mndict = {'minimumnorm_power':minnormpow,'minimumnorm_weights':w,'channels':res['channels']}
            self.data_file_selected['source_space'].update(mndict)
            self.updatestatusbar('minimum norm solution complete. added result to source_space.')
            self.refreshtree()
        MT = progressbar.MainThread()
        MT.main(minnormthread)

    def sourcesolution2img_handler(self,widget):
        obj=self.treedata;
        res = (self.setup_helper(var=['ind','data','img'],obj=obj));
        solution = self.treedata[self.selecteditem]
        c = sourcesolution2img.build(solution,ind=res['ind'],origimg=res['data'],img=res['img'])

        self.data_file_selected['source_space']['total_power'] = mean(c,axis=0);
        self.datadict[self.data_filename_selected] = self.data_file_selected
        self.updatestatusbar('solution to image complete')
        self.refreshtree()

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

    def filter_handler(self,widget):
        def donefilt(results):
            res['data_block'] = results
            self.result_helper(self.data_file_selected['filtered'],self.res)
            self.refreshtree()
        obj=self.treedata[self.selecteditem];
        res = self.res = (self.setup_helper(var=['data_block','srate','channels','numofepochs','labellist','chanlocs','frames','eventtime','wintime'],obj=obj));
        self.data_file_selected['filtered'] = {}
        self.fil = filter.filtwin()

        try:
            self.fil.setupfilterwin(None, res['data_block'],res['srate'],callback=donefilt)
        except KeyError:
            print('had a prob, bob')
            return -1
        self.fil.builder.get_object('FilterWindow').show()
        self.fil.builder.get_object('label1').set_text('Item to filter:'+str(self.selecteditem))

    def offset_handler(self,widget):
        def offset_callback(results):
            res['data_block'] = results
            self.result_helper(self.data_file_selected['offset_corrected'],self.res)
            self.updatestatusbar('offset correction complete')
            self.refreshtree()
        obj = self.obj = self.treedata[self.selecteditem];
        res = self.res = (self.setup_helper(var=['data_block','srate','channels','numofepochs','labellist','chanlocs','frames','eventtime','wintime'],obj=obj));
        self.offset = offset_correct.setup_gui()
        self.offset.setupoffsetwin(widget, res['data_block'],res['eventtime'],res['frames'],res['numofepochs'],callback=offset_callback)
        self.offset.window.show()
        self.data_file_selected['offset_corrected'] = {}

    def independent_component_analysis(self,widget):
        def ica_callback(results):
            self.data_file_selected['ica'] = self.res #results
            self.data_file_selected['ica']['data_block'] = results['weights']
            self.data_file_selected['ica']['activations'] = results['activations']
            #self.data_file_selected['ica']['labellist'] = results['labellist']
            #self.result_helper(self.data_file_selected['ica'],self.res)
            self.updatestatusbar('ica correction complete')
            self.refreshtree()
        obj=self.treedata[self.selecteditem];
        res = self.res = self.setup_helper(var=['data_block','channels','srate','wintime','labellist','chanlocs','numofepochs',\
        'frames','eventtime'],obj=obj)
        icawin = ica.setup(res['data_block'],callback=ica_callback)
        icawin.window.show()
        

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

        labels = []
        for i in range(0,size(ssp,1)):
            labels.extend(['SigSP'+str(i)])
        sp['labellist'] = labels

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
        print 'label state',self.mc.builder.get_object('channellabels').get_active()
        chanlocs = self.setup_helper(var='chanlocs',obj=self.treedata)['chanlocs']
        labellist = self.setup_helper(var='labellist',obj=self.treedata)['labellist']
        #if self.mc.builder.get_object('channellabels').get_active() == True:
            #self.mc.display(self.treedata[self.selecteditem],chanlocs, labels=labellist, subplot='on')
        #else:

        #Limit data to 50 subplots
        if shape(self.treedata[self.selecteditem])[0] > 50:
            print('Your data has too many indices, \n and this is an expensive function that you can not afford. Limiting you to the first 50 indices')
            self.errordialog('Your data has too many indices')
            data2plot = self.treedata[self.selecteditem][0:51]
        else:
            data2plot = self.treedata[self.selecteditem]
        self.mc.display(data2plot,chanlocs, subplot='on',labels=labellist)

    def result_helper(self,newobj,var):
        for i in var.keys():
            newobj[i] = var[i]
        return newobj

    def epoch_data(self,widget):
        def epoch_callback(widget,startcut,endcut):

            ed = self.data_file_selected['epoched_data'] = {}
            self.result_helper(ed,self.res)

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
                print (shape(tmp_data),shape(res['data_block'][i:j]))
                tmp_data[:,c] = res['data_block'][i:j]
                c = c+1
            print 'widgetname',widget.get_label()
            print 'elapsed time:',time.time()-ts
            avg_data = mean(tmp_data,axis=1)
            tmp_data = tmp_data.reshape((ed['frames']*len(startcut),size(ed['chanlocs'],1)),order='F')

            if widget.get_label() == 'Average':
                print 'Trying to average'
                tmp_data = avg_data;#mean(tmp_data.reshape((ed['frames'],len(startcut),size(ed['chanlocs'],1)),order='F'),axis=1)
                ed['wintime'] = arange(0,res['wintime'][ed['frames']],res['wintime'][1])
                ed['numofepochs'] = 1

            print ('tmpdatashape',shape(tmp_data))

            ed['data_block'] = tmp_data
            self.refreshtree()

        obj = self.obj = self.treedata[self.selecteditem]
        var = self.var = ['data_block','channels','srate','numofepochs','labellist','chanlocs','frames','eventtime','wintime']
        res = self.res = (self.setup_helper(var,obj=obj));

        #filepath = self.setup_helper(var='filepath',obj=self.treedata[self.selecteditem])['filepath']
        filepath = self.data_filename_selected
        if os.path.isfile(filepath) == False:
            return -1
        self.ed = event_process.setup_gui()
        self.ed.window.show()
        print ('sending file:'+'file://'+filepath)
        self.ed.set_passed_filename(filepath,callback=epoch_callback)
        self.ed.builder.get_object('filechooserbutton1').set_sensitive(False)

    def prerequisite(self,itemtype):
        print 'Item finder searching'
        menufunctions = self.builder.get_object('menufunctions').get_children()
        predict = {}
        try:
            if itemtype == 'selecteditem':
                obj=self.treedata[self.selecteditem]
                predict['Data Editor'] = ['data_block','srate','wintime','labellist','chanlocs']
                predict['Epoch Data'] = ['data_block','srate','wintime','labellist','chanlocs']
                predict['Time Freq Transform'] = ['data_block','labellist','srate','frames','numofepochs','eventtime']
                predict['Power Spectral Density'] = ['data_block','srate','labellist','chanlocs']
                predict['Filter'] = ['data_block','srate']
                predict['Offset Correct'] = ['data_block','srate']
                predict['Independant Component Analysis'] = ['data_block']


            if itemtype == 'generalitem':
                obj=self.treedata
                predict['Calculate Grid'] = ['hs']
                predict['Leadfield Calc'] = ['channels','grid']
                predict['Minimum Norm Solution'] = ['selection_event','leadfield','selection_noise','channels']
                predict['Solution To Image'] = ['ind','data','img']
                predict['Plot MRI'] = ['pixdim','data']
                predict['Contour Plot'] = ['chanlocs','labellist']
                predict['Plot TFT'] = ['tft']
                #predict['Plot'] = True



        except:
            #probably at home. no treedata to parse
            for j in menufunctions:
                if j.get_name() ==  'GtkMenuItem':
                    j.set_sensitive(False)

        for i in predict.keys():
            predict[i]
            try:
                r = self.setup_helper(var=predict[i],obj=obj);
                for j in menufunctions:
                    if j.get_name() ==  'GtkMenuItem' and j.get_label() == i:
                        j.set_sensitive(True)

            except KeyError:
                for j in menufunctions:
                    if j.get_name() ==  'GtkMenuItem' and j.get_label() == i:
                        j.set_sensitive(False)

        try:
            if type(self.treedata[self.selecteditem]) == ndarray:
                for j in menufunctions:
                    if j.get_label() == 'Plot' or j.get_label() == 'Contour Plot':
                        j.set_sensitive(True)
            else:
                for j in menufunctions:
                    if j.get_label() == 'Plot' or j.get_label() == 'Contour Plot':
                        j.set_sensitive(False)
        except:
            pass

    def data_editor(self, widget):
        def data_editor_callback(widget):
            print ('de calling back'), widget.get_label()
            try:
                data = self.de.data
                if widget.get_label() == 'Save As Event':
                    self.de.get_time_selection(widget,current=True)
                    self.data_file_selected['selection_event'] = data[self.de.sel_ind]
                if widget.get_label() == 'Save As Noise':
                    self.de.get_time_selection(widget,current=True)
                    self.data_file_selected['selection_noise'] = data[self.de.sel_ind]
                print 'saved selection....'
                if widget.get_label() == 'Offset Correct':
                    print 'replacing data with offset correction'
                    try:
                        self.obj.data_block = data
                        print 'replaced'

                    except:
                        print 'error replacing'
                if widget.get_label() == 'Filter':
                    pass

            except:
                pass
            self.refreshtree()

        try:
            self.obj = obj=self.treedata[self.selecteditem];
            res = (self.setup_helper(var=['data_block','srate','wintime',
            'labellist','chanlocs'],obj=obj));
            print (len(res))
            print res.keys()

        except:
            print ("Data Editor can't handle this type")
            print ("Try selecting object <pdf2py.data.read>")
            self.errordialog("Data Editor can't handle this type.Try selecting object <pdf2py.data.read> ");
            return -1

        try:
            self.de = data_editor.setup_gui()
            #self.de.data_handler(r[0],r[1],r[2],r[3],r[4], callback=self.data_editor_callback)
            self.de.data_handler(widget, input_dict=res, callback=data_editor_callback)
            self.de.window.show()
        except RuntimeError:
            self.errordialog("Can't do that Dave");

    def power_spectral_density(self,widget):
        obj=self.treedata[self.selecteditem];
        res = (self.setup_helper(var=['data_block','srate','labellist','chanlocs'],obj=obj));
        self.psd = power_spectral_density.setup_gui()
        self.psd.datahandler(res)
        self.psd.window.show()

    def spin(self, status):
        try: print self.spinner_gui.window.get_visible()
        except: self.spinner_gui = spinner.setup()
        if status == 'start':
            self.spinner_gui.start()
            self.spinner_gui.window.show()

        if status == 'stop':
            self.spinner_gui.stop()
            self.spinner_gui.window.hide()

    def testhandler(self, widget):
        self.prnt(None)
        self.timef_handler(None)

    def testload(self, fn):
        print('clicked')
        from gui.gtk import parse_instance
        fns = [fn] #['/home/danc/python/data/0611/0611piez/e,rfhp1.0Hz,COH']

        for i in fns:
            print('i', i)
            self.fn = path = i
            self.datadict[path] = pdf.read(self.fn)
            self.datadict[path].data.setchannels('meg')
            self.datadict[path].data.getdata(0, self.datadict[path].data.pnts_in_file)
            self.chanlist = ['meg']
            self.readMEG()
        #self.fn = ['/home/danc/programming/python/data/standardmri/colin_1mm.img']
        ##self.datadict[path] = self.fn
        #self.filetype = 'MRI'
        #self.builder.get_object("filechooserdialog").set_uri('file://'+self.fn[0])
        #self.builder.get_object("filechooserdialog").show()

class MainThread(threading.Thread):
    def run(self):
        gtk.gdk.threads_init()
        self.builder = gtk.Builder()
        self.builder.add_from_file("progressbar.glade")
        self.pbwindow = self.builder.get_object("window1")
        self.progressbar = self.builder.get_object("progressbar")
        self.pbwindow.show()
        self.progressbar.show()
        self.pbwindow.connect('destroy', gtk.main_quit)
        self.still_working = True
        gobject.timeout_add(100, self.pulse)
        self.tic = 0
        gtk.main()

    def pulse(self):
        self.progressbar.pulse()
        return self.still_working # 1 = repeat, 0 = stop

    def test(self,widget):
        pass

    def terminate(self):
        self.still_working = False
        self.pbwindow.hide()

    def interaction_shell(self,widget):
        import code; code.interact(local=locals()) #Interactive Shell

if __name__ == "__main__":
    import cProfile, pstats
    #cProfile.run('mainwindow = maingui()')
    mainwindow = maingui()
    #mainwindow.window.show()
    mainwindow.testload('/home/danc/data/meg/0611piez/e,rfhp1.0Hz,ra.mod')#/home/danc/data/meg/0611piez/e,rfhp1.0Hz,ra.mod')
    #cProfile.run('mainwindow.testload(None)')
    #import code; code.interact(local=locals()) #Interactive Shell
    gtk.main()




