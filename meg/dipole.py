'''point density'''

from meg import euclid
from numpy import size, zeros, array, inf, shape, sum, mean
import wx
import os

#poximity based density method
#def proximity(points, scale=None):
def density(points):
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
            dist = 1/euclid.dist(
            points[i,0], points[ii,0],\
            points[i,1], points[ii,1], \
            points[i,2], points[ii,2]);

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
    for i in range(0, size(voxel,1)): #3XN
        #for each dipole im mri coords
        r1 = round(voxel[0,i])
        r2 = round(voxel[1,i])
        r3 = round(voxel[2,i])
        print r1,r2,r3, sumvalue[i]
##        print emptymri[r1,r2,r3]
##        print sumvalue[i]

        try:
            emptymri[r1,r2,r3] = sumvalue[i]
        except IndexError: #possibly dipole outside mri space
            print 'warning, possible dipole #',i,'outside field of view'



    return emptymri
    #f = ndimage.gaussian_filter(z, 14)

def readdipolefile(self):
    dlg = wx.FileDialog(self, "Select a meg 4d type dipole textfile", os.getcwd(), "", "*", wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
        filepath = path = dlg.GetPath()
        dlg.Destroy()
        return filepath

class parsereport:
    def __init__(self,filepath):
        #filepath = '/home/danc/python/data/E-0043dipoledensityTEST'

        file = open(filepath,"r")
        #positioncheck = 1
        diparray = []
        while True:
            firstposition = file.tell();
            diparray.append(file.readline())
            nextposition = file.tell();
            if firstposition == nextposition:
                break

        for i in range(0, size(diparray)):
            if diparray[i].find('MR/CT') != -1: #MR overlay report, skip only one line
                skipval = 2

            if diparray[i].find('Latency') != -1:
                fields = diparray[i].split()

                try:
                    newarray = diparray[i+skipval:-1] #MR/CT report, skip to dipole parameters
                    print 'file read as MR/CT report. skipping 2 lines from end of header'
                except NameError:
                    newarray = diparray[i+4:-1] #Dipole report, skip to dipole parameters
                    print 'file read as dipole report. skipping 4 lines from end of header'

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
    points = array([[0,0,40],[100,0,0],[1,2,3],[1,2,5],[1,2,10]])
    x=calc(points)
    print x

'''
#split file containing multiple MRO dipole files in it
ind = []
for i in range(0,len(l)):
    try:
        b = l[i].index('Disk Media:')
        ind.append(i)

    except ValueError:
        pass

for j in range(0, len(ind-1)):
    d = l[ind[j]:ind[j+1]]
    fn = l[ind[j]+2].split(':')[1].replace('\n','').strip(' ')
    f = open(fn+'.drf','w')
    f.writelines(d)
    f.close()
'''
