'''mr2vtk'''
from pyvtk import *
from numpy import *
import os

def convert(mrdata, data2=None, path='~/', filename=None):
    '''convert(mrdata, data2=None, path='~/', filename=None)'''
    if filename == None:
        print 'need a filename specified'
        print convert.__doc__
        return
    data1 = mrdata.data
    print 'processing first dataset'
    d1 = float32(reshape(data1, (-1), order='F'))
    resultimg = d1
    if data2 != None:
        if data1.shape != data2.shape:
            print 'mismatch between the 2 datasets shape. exiting'
            return
        print 'second dataset assumed to be underlay'
        d2 = float32(reshape(data2, (-1)))
        print 'scaling underlay values to overlay range'
        print 'scale factor ',d1.max()/d2.max()
        d2s = d2*(d1.max()/d2.max())
        d1d2 = (d1+d2s)/2
        resultimg = d1d2


    shapeofimg = data1.shape
    print shapeofimg, resultimg.shape
    print 'converting data'
    vtkdata = VtkData(StructuredPoints([shapeofimg[0],shapeofimg[1],shapeofimg[2]]), PointData(Scalars(resultimg)))
    vtkdata.structure.spacing = mrdata.voxdim[::-1]

    if path == '~/':
        print 'writing file ', os.getenv('HOME')+'/'+filename+'.vtk'
        vtkdata.tofile(os.getenv('HOME')+'/'+filename, 'binary')
    else:
        print 'writing file ', path+filename+'.vtk'
        vtkdata.tofile(path+filename, 'binary')

    #return vtkdata, resultimg

if __name__ == "__main__":
    def __init__(self):
        convert()
