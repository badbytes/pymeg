#       scatter_wregression.py
#
#       Copyright 2010 danc <danc@badbytes.net>
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

from pylab import *

def plotdata(diag,data1,data2,label1, label2):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    colors = ['b','g','r','c','k','y','m']
    markers = ['s','o','^','d']
    colors = colors[::-1]
    for dx in unique(diag):
        d1 = data1[diag == dx]
        d2 = data2[diag == dx]
        c = colors.pop()
        m = markers.pop()

        (ar,br)=polyfit(d1,d2,1)
        xr=polyval([ar,br],d1)
        t=linspace(d1.min(),d1.max(),len(d1))

        #ax.scatter(d1,d2, s=50,color=c, marker=m, alpha=.6, label=dx)
        ax.set_xlabel(label1, fontsize=10)
        ax.set_ylabel(label2, fontsize=10)
        ax.set_title(label2 +' vs '+label1)
        ax.grid(True)

        mn = where(d1 == d1.min())
        mx = where(d1 == d1.max())
        #ax.plot(data1,xr,linestyle='dashed')#'r.')
        ax.plot([d1.min(),d1.max()],[xr[mn],xr[mx]],color=c,linestyle='dashed')#'r.')
        ax.scatter(d1,d2, s=60,color=c, marker=m, alpha=.6, label=dx)
    #ax.legend(unique(diag), scatterpoints=0)
    ax.legend(scatterpoints=1, numpoints=1)

    #ax.plot(data1,xr,'r---')

    show()

if __name__ == '__main__':
    d = readspreadsheet.readcsv('BrainVolumeSummary_AgeCutoff58.csv',',')
    vars = ['Ventricle Brain Ratio','GWR','Total Brain Volume','Brain ICV Ratio','Ventricular CSF']
    data1 = d['Age at MRI']
    scatter_wregression.plotdata(d['Diagnosis'],data1,d[vars[0]],'Age',vars[0])

    pass
