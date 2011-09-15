#       density.py
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
'''density calc returns the 1/euclid distance of the cartesian points supplied.
returns the distance square matrix of size numofpointsXnumofpoints.
ex.
c = array([[1, 1, 1],
           [2, 2, 2],
           [3, 3, 3],
           [2, 2, 2]])

density.calc(c)

Out[50]:
array([[ 0.        ,  0.57735027,  0.28867513,  0.57735027],
       [ 0.57735027,  0.        ,  0.57735027,  1.        ],
       [ 0.28867513,  0.57735027,  0.        ,  0.57735027],
       [ 0.57735027,  1.        ,  0.57735027,  0.        ]])


'''

from meg import euclid
from numpy import size, zeros, array, inf, shape, sum, mean
#import wx
import os

#poximity based density method
#def proximity(points, scale=None):
def calc(points):
    '''scale is the slice thickness
    if 3D and non cubic then scale'''
    if size(shape(points)) != 2:
        print 'error in points dimensions'
    if shape(points)[1] != 3:
        if shape(points)[0] != 3:
            print 'something wrong'
            return
        else: #transpose
            print 'transposing'
            points = points.T
    distmat=zeros([size(points ,0), size(points ,0)]);
    for i in range(0,size(points,0)):# %get euclid dist between all pairs of points
        for ii in range(0,size(points ,0)):
            dist = 1/euclid.dist(points[i], points[ii])
            #points[i,1], points[ii,1], \
            #points[i,2], points[ii,2]);

            if dist == inf:
                if i == ii:
                    distmat[i,ii] = 0
                else:
                    distmat[i,ii] = 1
            else:
                distmat[i,ii] = dist
    

    return distmat

def val2img(mrdata, value, voxel):
    '''mrdata is the mri
    value is the value (eg diploe density)
    voxel is the coordinate of the voxel (eg. 91.89179704,  99.24560901,  64.40871847)'''

    if size(voxel,0) != 3:
        print 'array shape wrong'
        return

    emptymri = zeros(mrdata.shape)
    sumvalue = mean(value, axis=0)
    for i in range(0, size(voxel,1)): #3XN for each dipole in mri coords
        r1 = round(voxel[0,i])
        r2 = round(voxel[1,i])
        r3 = round(voxel[2,i])
        print r1,r2,r3, sumvalue[i]
        try:
            emptymri[r1,r2,r3] = sumvalue[i]
        except IndexError: #possibly dipole outside mri space
            print 'warning, possible dipole #',i,'outside field of view'
    return emptymri

#def readdipolefile(self):
    #dlg = wx.FileDialog(self, "Select a meg 4d type dipole textfile", os.getcwd(), "", "*", wx.OPEN)
    #if dlg.ShowModal() == wx.ID_OK:
        #filepath = path = dlg.GetPath()
        #dlg.Destroy()
        #return filepath

class parsedipolereport:
    def __init__(self,filepath):
        file = open(filepath,"r")
        diparray = []
        while True:
            firstposition = file.tell();
            diparray.append(file.readline())
            nextposition = file.tell();
            if firstposition == nextposition:
                break

        for i in range(0, size(diparray)):
            if diparray[i].find('Latency') == 1:
                fields = diparray[i].split()
                newarray = diparray[i+4:] #only dipole properties
                numdips = size(newarray) #num of dipoles
                numprop = size(newarray[0].split()) #size of fields
                s = zeros([numdips, numprop])# empty matrix

                for n in range(0, size(newarray)): #i+4 finds first dipole location from header
                    try:
                        s[n,:] = array(newarray[n].split())
                    except ValueError:
                        #print 'dip line not right' #if its a dipole report then can't handle strings and literals
                        #try to get the first 13 columns
                        #return s, newarray
                        try:
                            s[n,0:13] = array(newarray[n].split()[0:13])
                        except ValueError:
                            pass

                try: fields.remove('||')
                except ValueError: pass
                try: fields.remove('||')
                except ValueError: pass
                break
        self.dips = s
        self.labels = fields



if __name__ == '__main__':
    points = array([[0,0,40],[100,0,0],[0,0,0]])
    x=calc(points)
    print x
