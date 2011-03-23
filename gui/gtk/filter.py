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

class filtwin:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("filter.glade")
        self.window = self.builder.get_object("FilterWindow")

        dic = {
            "startfiltfilt" : self.startfiltfilt,
            "on_updatefiltbox" : self.updatefiltbox,
            }

        self.builder.connect_signals(dic)

    def test(self,widget):
        print 'test'

    def datahandler(data=None):
        self.data = data


    def setupfilterwin(self, widget, workspace_data=None, data_selected=None):
        print 'filter stuff'
        self.workspace_data = workspace_data
        self.data_selected = data_selected
        self.hdr = workspace_data.data.hdr
        self.builder.get_object('FilterWindow').show()
        try:
            self.builder.get_object('entry24').set_text(str(1/self.hdr.header_data.sample_period[0]))
            #self.builder.get_object('entry24').set_text(str(1/self.datadict[self.fn].data.hdr.header_data.sample_period[0]))
        except AttributeError:
            print 'no header loaded'
        self.updatefiltbox(self)

    def updatefiltbox(self,box):
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
        srate = float(self.builder.get_object('entry24').get_text())
        order = int(self.builder.get_object('entry27').get_text())
        self.filter_results = filtfilt.calc(self.data_selected, srate, self.Wn, order, self.band)
        #return self.filter_results
        self.workspace_data.results.fil = self.filter_results


if __name__ == "__main__":
    mainwindow = filtwin()
    mainwindow.window.show()
    gtk.main()
