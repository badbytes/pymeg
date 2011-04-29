'''reconstruct mri out of source result'''
# Copyright 2008 Dan Collins
#
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# And is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Build; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#090327 added ndimage module from scipy to make compatible with python 2.6


from numpy import zeros,shape,size, array, squeeze
from mri import interp_array
import sys
try:
    import ndimage
except ImportError:
    from scipy import ndimage

def build(sourcedata, sourcespace, hisample=None):
    '''[decimg, hiresimg] = sourcesolution2img(w.corr_mat, dec)'''
    '''sourcedata = w.corr_mat
    sourcespace = dec
    ie, dec = img.decimate(nimstripped, 20)
    lf = leadfield.calc(p.data.channels, grid=i.megxyz)
    '''
    if size(sourcedata,1) != size(sourcespace.ind,1):
        print('mismatch between sourcedata and sourcespace indices. They are diff lengths and this wont make sense. exiting.')
        return

    if size(sourcedata.shape) == 1: #make 2D
        sourcedata = array([sourcedata])

    print 'size of new sourcedata is', shape(sourcedata)
    print (size(sourcespace.img,0),size(sourcespace.img,1),size(sourcespace.img,2), size(sourcedata,0))
    print 'size of new sourcespace is', shape(sourcespace.img)

    newimg = zeros((size(sourcedata,0), size(sourcespace.img,0),size(sourcespace.img,1),size(sourcespace.img,2)))
    print 'size of new img is', shape(newimg)


    #for ii in range(0, size(sourcedata,0)): #for each component

    for j in range(0, size(sourcedata,0)): #for each component
        print 'processing component',j
        for i in range(0, size(sourcedata,1)): #for each location
            newimg[j,sourcespace.ind[0,i],sourcespace.ind[1,i],sourcespace.ind[2,i]] = sourcedata[j,i];
    #del sourcedata#, sourcespace.mrixyz, sourcespace.ind, sourcespace.img
    #resample back to original resolution
    newshape = [size(newimg,0),sourcespace.nifti.data.shape[0],sourcespace.nifti.data.shape[1],\
    sourcespace.nifti.data.shape[2]]




    if hisample != None:
        print 'resampling back to original. From', shape(newimg), 'to', size(newimg,0),sourcespace.nifti.data.shape
        hiresimg = zeros((newshape));print shape(hiresimg)
        print shape(hiresimg)
        for k in range(0,size(newimg,0)):
            print 'hires resample of index', k, 'of', size(newimg,0)
            hiresimg[k,:,:,:] = interp_array.rebin(squeeze(newimg[k,:,:,:]), sourcespace.nifti.data.shape)
        #return hiresimg
        print 'filtering image'
        return newimg, hiresimg#f

    else:
        return newimg

    #~ #filthires = ndimage.gaussian_filter(hiresimg, 4)#, order=2)
    #~ voxdim = sourcespace.nifti.voxdim
    #~ sigma = 2
    #~ f = ndimage.gaussian_filter1d(hiresimg, sigma*1/ voxdim[2], axis=0)
    #~ f = ndimage.gaussian_filter1d(f, sigma*1/ voxdim[1], axis=1)
    #~ f = ndimage.gaussian_filter1d(f, sigma*1/ voxdim[0], axis=2)


    #return newimg, hiresimg#f

