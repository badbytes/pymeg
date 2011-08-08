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
import sys,os,mdp
from numpy import *
from pylab import *

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

'''approach='defl', g='pow3', guess=None, fine_g='pow3', mu=1,
stabilization=False, sample_size=1, fine_tanh=1, fine_gaus=1, max_it=1000,
max_it_fine=100, failures=5, limit=0.001, verbose=False, whitened=False, white_comp=None,
white_parm=None, input_dim=None, dtype=None)'''

class setup:
    def __init__(self,data=None,callback=None):
        self.callback = callback
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("window")

        dic = {
            "on_button_apply_clicked" : self.get_opts,
            }

        self.builder.connect_signals(dic)
        self.data = data
        #self.channels = channels
        
    def get_opts(self,widget):
        opts = {}
        print 'hello'
        names = self.builder.get_object("box_names").get_children()
        vals = self.builder.get_object("box_values").get_children()
        for i in arange(len(vals)):
            if vals[i].get_name() == 'GtkComboBox':
                res = vals[i].get_active_text()
            if vals[i].get_name() == 'GtkEntry':
                try: res = float32(vals[i].get_text())
                except ValueError: res = vals[i].get_text()

            opts[names[i].get_text()] = res

        print opts


        #Run ICA
        ica = mdp.nodes.FastICANode(white_comp=opts['white_comp'],approach=opts['approach'], g=opts['g'], fine_g=opts['fine_g'],\
        mu=opts['mu'], stabilization=opts['stabilization'], sample_size=opts['sample_size'], fine_tanh=opts['fine_tanh'], fine_gaus=opts['fine_gaus'], \
        max_it=int(opts['max_it']), max_it_fine=int(opts['max_it_fine']), failures=opts['failures'], limit=opts['limit'],verbose=True)
        #, whitened=opts['whitened'])#, \
        #white_parm=opts['white_parm'])

        '''ica = mdp.nodes.FastICANode(white_comp=10,approach='defl', g='pow3', guess=None, fine_g='pow3', mu=1, stabilization=False, sample_size=1, fine_tanh=1, fine_gaus=1, max_it=10000, max_it_fine=100, failures=5, limit=0.001, verbose=True)'''


        ica.train(self.data)
        comp = ica.execute(self.data)
        #z = dot(self.data,ica.get_recmatrix().T)
        #z = z-z[0]
        labels = []
        for i in arange(size(comp,1)):
            labels = append(labels,'comp'+str(i))
        print 'done'
        
        results = {'weights':comp,'activations':ica.get_recmatrix(),'labellist':labels}
        try: self.callback(results)
        except: return results
        
        
        #subplot(2,1,1)
        #plot(comp);
        #subplot(2,1,2)
        #plot(self.data-self.data[0]);
        #show()

if __name__ == "__main__":
    from pdf2py import pdf
    p = pdf.read('/home/danc/data/meg/0611piez/e,rfhp1.0Hz,ra,f50lp,o')
    p.data.setchannels('meg')
    p.data.getdata(0,p.data.pnts_in_file)


    mainwindow = setup(data=p.data.data_block)
    mainwindow.window.show()

    print('testing')
    gtk.main()
