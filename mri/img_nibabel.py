# Copyright 2008 Dan Collins

# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# And is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Build; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

'''New image read method.
mr = img.loadimage('image.nii.gz') #loads nifti
mr.decimate(10) #reduces mr grid to a factor of 10 or other
mr.scalespace(path2pdf) #scales MR image space to pdf headshape
mr.fitdata(path2pdf, 10, weights) #fits weights to a grid a factor of 10
'mr.fitresult.corr_mat = correlationresult'
mr.getsourcesolution() #generates a low and hires mri like image of the fit over decimated sourcespace
'''

from numpy import ceil, shape, where, array, ndarray
#from nifti import *
from mri import transform, sourcesolution2img
from pdf2py import readwrite


import nibabel,os #import nifti1 as nifti

class loadimage():
    def __init__(self, filepath):
        print 'reading',filepath
        self.nifti = nibabel.load(filepath)
        dirpath = os.path.dirname(filepath)
        if os.path.isfile(filepath+'.pym') == True:
            self.fiddata = readwrite.readdata(filepath+'.pym')
            self.getfiducals()
        else:
            print 'no fiducal file'

    def getfiducals(self):
        self.lpa = self.fiddata['lpa']
        self.rpa = self.fiddata['rpa']
        self.nas = self.fiddata['nas']

    def decimate(self, dec):
        '''nim is the mri data in python format
        dec is the decimation factor'''

        nim = self.nifti
        header = nim.get_header()
        self.filename = nim.get_filename()
        xend = nim.get_shape()[0]
        yend = nim.get_shape()[1]
        zend  =nim.get_shape()[2]

        if type(dec) != float and type(dec) != int:
            print 'nonuniform decimation'
            xstartval=ceil(dec[0]/2);
            print xstartval,
            ystartval=ceil(dec[1]/2);
            zstartval=ceil(dec[2]/2);
            decimg=array(nim.data[xstartval::dec[0],:,:][:,ystartval::dec[1],:][:,:,zstartval::dec[2]])
            nonz = where(decimg > 0)
            x = ((nonz[0])*dec[0])+(dec[0])
            y = ((nonz[1])*dec[1])+(dec[1])
            z = ((nonz[2])*dec[2])+(dec[2])

        else:
            print 'uniform decimation'
            startval=ceil(dec/2);
            decimg=array(nim.get_data()[startval::dec,:,:][:,startval::dec,:][:,:,startval::dec])
            nonz = where(decimg > 0)
            x = ((nonz[0]+1)*dec)#-(dec)
            y = ((nonz[1]+1)*dec)#-(dec)
            z = ((nonz[2]+1)*dec)#-(dec)


        #--20090702--danc--not sure about reordering
        #mrixyz = array([x,y,z])
        #--20090702--danc--adding voxel scaling. this had to be a huge bug, so why i haven't noticed it so far???
        #                   The effect would be non existant on isotropic volumes, so thats probably why.

        voxdim = header['pixdim'][0:3]#.voxdim[::-1] #flipped voxel dims
        print voxdim
        #print 'WARNING: assuming voxdim reverse of img.voxdim. Could be wrong'
        mrixyz = (array([x,y,z]).T*voxdim).T

        self.mrixyz = mrixyz
        self.img = decimg
        self.factor = dec
        self.ind = array(nonz)

        try:

            [t,r] = transform.meg2mri(self.lpa,self.rpa,self.nas)
            self.megxyz = transform.mri2meg(t,r,self.mrixyz)
        except AttributeError:
            pass

    def getscalespace(self, path2pdf):
        self.scaledgrid = transform.scalesourcespace(path2pdf, self.megxyz, self.lpa, self.rpa, self.nas, self.nifti.voxdim)/1000
        self.path2pdf = path2pdf

    def getsourcesolution(self, highres=None):
        if highres != None:
            [self.lowres, self.hires] = sourcesolution2img.build(self.fitresult.corr_mat, self,hisample='yes')
        else:
            self.lowres = sourcesolution2img.build(self.fitresult.corr_mat)

    def getleadfield(self):
        from meg import leadfield
        from pdf2py import pdf
        p = pdf.read(self.path2pdf);p.data.setchannels('meg')
        self.lf = leadfield.calc(self.path2pdf, p.data.channels, self.scaledgrid*1000)

    def getcorrelationfit(self, weights):
        from meg import weightfit
        try:
            self.lf
        except:
            print('no leadfields detected. one time generation')
            self.getleadfield()

        self.fitresult = weightfit.calc(self.path2pdf, self.lf.leadfield, weights)

    def fitdata(self, path2pdf, decimationfactor, weights): #script to
        try:
            self.factor
            if self.factor != decimationfactor:
                del(self.lf)
        except:
            pass
        self.decimate(decimationfactor)
        self.getscalespace(path2pdf)
        self.getcorrelationfit(weights)



### OLD STUFF BELOW. LEFT FOR COMPATIBILITY.
def ind2sub(row,col,ind):
    """ Converts row,col indices into one index for .flat """
    i = ind/col
    j = ind - i* row
    return i,j

def read(imgfile):
    print 'reading',imgfile
    #try:
    nim = NiftiImage(imgfile)
    return nim
    #except RuntimeError:
        #print 'not an mri, or file corrupt. not loading!'
        #return MRIerror

class decimate:
    def __init__(self,nim,dec):
#def decimate(nim, dec):
        "nim is the mri data in python format"
        "dec is the decimation factor"

        self.filename = nim.filename.rsplit('/')[-1]
        xend=shape(nim.data)[0]
        yend=shape(nim.data)[1]
        zend=shape(nim.data)[2]

        if type(dec) != float and type(dec) != int:
            print 'nonuniform decimation'
            xstartval=ceil(dec[0]/2);
            print xstartval,
            ystartval=ceil(dec[1]/2);
            zstartval=ceil(dec[2]/2);
            decimg=array(nim.data[xstartval::dec[0],:,:][:,ystartval::dec[1],:][:,:,zstartval::dec[2]])
            nonz = where(decimg > 0)
            x = ((nonz[0])*dec[0])+(dec[0])
            y = ((nonz[1])*dec[1])+(dec[1])
            z = ((nonz[2])*dec[2])+(dec[2])

        else:
            print 'uniform decimation'
            startval=ceil(dec/2);
            decimg=array(nim.data[startval::dec,:,:][:,startval::dec,:][:,:,startval::dec])
            nonz = where(decimg > 0)
            x = ((nonz[0]+1)*dec)#-(dec)
            y = ((nonz[1]+1)*dec)#-(dec)
            z = ((nonz[2]+1)*dec)#-(dec)


        #--20090702--danc--not sure about reordering
        #mrixyz = array([x,y,z])
        #--20090702--danc--adding voxel scaling. this had to be a huge bug, so why i haven't noticed it so far???
        #                   The effect would be non existant on isotropic volumes, so thats probably why.
        voxdim = nim.voxdim[::-1] #flipped voxel dims
        print voxdim
        print 'WARNING: assuming voxdim reverse of img.voxdim. Could be wrong'
        mrixyz = (array([x,y,z]).T*voxdim).T

        self.mrixyz = mrixyz
        self.img = decimg
        self.factor = dec
        self.ind = array(nonz)
        self.origimg = nim

if __name__ == "__main__":
    def __init__(self):
        self.nim=read()
        self.dec=decimate(self.nim, 5)

