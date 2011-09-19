#!/usr/bin/python2


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

from numpy import ceil, shape, where, array, ndarray, copy
#from nifti import *
from mri import transform, sourcesolution2img
from pdf2py import readwrite


import nibabel,os #import nifti1 as nifti

class loadimage():
    def __init__(self, filepath):
        print 'reading',filepath
        self.nifti = nibabel.load(filepath)
        dirpath = os.path.dirname(filepath)
        self.data = copy(self.nifti.get_data())#.T
        #self.nifti.data = self.data
        h = self.nifti.get_header()
        self.pixdim = h['pixdim'][1:4]
        self.gettransform(h)
        #self.reorient()
        xfm_fn = os.path.splitext(filepath)[0]+'.pym'
        if os.path.isfile(xfm_fn) == True:
            print('loading index points found in file',xfm_fn)
            self.fiddata = readwrite.readdata(xfm_fn)
            self.getfiducals(h)
        else:
            try: #This is a shitty way in which fiducal point were saved in descrip field in header, as there were no user avail fields to store the 3X3 matrix.
                self.lpa# = eval(str(h['descrip']))[0]
                self.rpa# = eval(str(h['descrip']))[1]
                self.nas# = eval(str(h['descrip']))[2]
                print('got fiducal info from description field in header')
            except:
                print 'no fiducal file or info found. you will not be able to perform any transforms with other data.'

    #def reorient(self):
        #'''27 possible combinations of orientations
        #('LAI' or 'LIA' or 'ALI' or 'AIL' or 'ILA' or 'IAL' or 'LAS' or 'LSA' or 'ALS' or 'ASL' or 'SLA' or 'SAL' or 'LPI' or 'LIP' or 'PLI' or 'PIL' or 'ILP' or 'IPL' or 'LPS' or 'LSP' or 'PLS' or 'PSL' or 'SLP' or 'SPL' or 'RAI' or 'RIA' or 'ARI' or 'AIR' or 'IRA' or 'IAR' or 'RAS' or 'RSA' or 'ARS' or 'ASR' or 'SRA' or 'SAR' or 'RPI' or 'RIP' or 'PRI' or 'PIR' or 'IRP' or 'IPR' or 'RPS' or 'RSP' or 'PRS' or 'PSR' or 'SRP' or 'SPR')'''
        #print 'transform',self.transform[:,0],abs(self.transform[:,0]).argmax(),
        #self.t = copy(self.translation)

        #rot = self.transform[0:3,0:3]
        #arot = abs(rot)
        #print arot
        #if abs(rot[:,0]).argmax() == 0: #RL first dim
            ##if rot[0,0] < 0:
                ##self.data = self.data[::-1,:,:]
                ##rot[0,0] = rot[0,0] * -1
                ##print 'flipping'
            #print 'swapping'
            #self.data = self.data.swapaxes(0,1)
            #self.t[0] = self.translation[1]; self.t[1] = self.translation[0]
            #rot[0,:] = rot[0,]
        #if arot[:,0].argmax() == 1: #AP first dim
            ##self.origimg = self.origimg.swapaxes(0,1)
            #pass

        #if arot[:,1].argmax() == 1: #AP second dim
            #if rot[0,1] < 0:
                #self.data = self.data[::-1,:,:]
            #pass
        #if arot[:,2].argmax() == 2: #IS third dim
            #pass
        #if self.transform[:,0:4].argmax() == 2: #IS first dim
            #pass

    def getfiducals(self,header):
        self.lpa = self.fiddata['lpa']
        self.rpa = self.fiddata['rpa']
        self.nas = self.fiddata['nas']

    def gettransform(self,header):
        print 'Affine Transform is'
        print header.get_base_affine()
        self.transform = header.get_base_affine()
        self.translation = self.transform[0:3,3]#[::-1]

    def decimate(self, dec):
        '''nim is the mri data in python format
        dec is the decimation factor'''

        #nim = self.nifti
        header = self.nifti.get_header()
        self.filename = self.nifti.get_filename()
        xend = self.nifti.get_shape()[0]
        yend = self.nifti.get_shape()[1]
        zend = self.nifti.get_shape()[2]

        if type(dec) != float and type(dec) != int:
            print 'nonuniform decimation'
            xstartval=ceil(dec[0]/2);
            print xstartval,
            ystartval=ceil(dec[1]/2);
            zstartval=ceil(dec[2]/2);
            decimg=array(self.data[xstartval::dec[0],:,:][:,ystartval::dec[1],:][:,:,zstartval::dec[2]])
            nonz = where(decimg > 0)
            x = ((nonz[0])*dec[0])+(dec[0])
            y = ((nonz[1])*dec[1])+(dec[1])
            z = ((nonz[2])*dec[2])+(dec[2])

        else:
            print 'uniform decimation'
            startval=ceil(dec/2);
            decimg=array(self.data[startval::dec,:,:][:,startval::dec,:][:,:,startval::dec])
            nonz = where(decimg > 0)
            x = ((nonz[0]+1)*dec)#-(dec)
            y = ((nonz[1]+1)*dec)#-(dec)
            z = ((nonz[2]+1)*dec)#-(dec)


        #--20090702--danc--not sure about reordering
        #mrixyz = array([x,y,z])
        #--20090702--danc--adding voxel scaling. this had to be a huge bug, so why i haven't noticed it so far???
        #                   The effect would be non existant on isotropic volumes, so thats probably why.

        voxdim = header['pixdim'][1:4]#.voxdim[::-1] #flipped voxel dims
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
            print 'Transform Error, skipping'

    def getscalespace(self, path2pdf):
        self.scaledgrid = transform.scalesourcespace(path2pdf, self.megxyz, self.lpa, self.rpa, self.nas, self.nifti.voxdim)#/1000
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

    def savefile(self,filepath):
        self.nifti.to_filename(filepath+'test.nii.gz')


#### OLD STUFF BELOW. LEFT FOR COMPATIBILITY.
#def ind2sub(row,col,ind):
    #""" Converts row,col indices into one index for .flat """
    #i = ind/col
    #j = ind - i* row
    #return i,j

#def read(imgfile):
    #print 'reading',imgfile
    ##try:
    #nim = NiftiImage(imgfile)
    #return nim
    ##except RuntimeError:
        ##print 'not an mri, or file corrupt. not loading!'
        ##return MRIerror

#class decimate:
    #def __init__(self,nim,dec):
##def decimate(nim, dec):
        #"nim is the mri data in python format"
        #"dec is the decimation factor"

        #self.filename = nim.filename.rsplit('/')[-1]
        #xend=shape(nim.origimg)[0]
        #yend=shape(nim.origimg)[1]
        #zend=shape(nim.origimg)[2]

        #if type(dec) != float and type(dec) != int:
            #print 'nonuniform decimation'
            #xstartval=ceil(dec[0]/2);
            #print xstartval,
            #ystartval=ceil(dec[1]/2);
            #zstartval=ceil(dec[2]/2);
            #decimg=array(nim.origimg[xstartval::dec[0],:,:][:,ystartval::dec[1],:][:,:,zstartval::dec[2]])
            #nonz = where(decimg > 0)
            #x = ((nonz[0])*dec[0])+(dec[0])
            #y = ((nonz[1])*dec[1])+(dec[1])
            #z = ((nonz[2])*dec[2])+(dec[2])

        #else:
            #print 'uniform decimation'
            #startval=ceil(dec/2);
            #decimg=array(nim.origimg[startval::dec,:,:][:,startval::dec,:][:,:,startval::dec])
            #nonz = where(decimg > 0)
            #x = ((nonz[0]+1)*dec)#-(dec)
            #y = ((nonz[1]+1)*dec)#-(dec)
            #z = ((nonz[2]+1)*dec)#-(dec)


        ##--20090702--danc--not sure about reordering
        ##mrixyz = array([x,y,z])
        ##--20090702--danc--adding voxel scaling. this had to be a huge bug, so why i haven't noticed it so far???
        ##                   The effect would be non existant on isotropic volumes, so thats probably why.
        #voxdim = nim.voxdim[::-1] #flipped voxel dims
        #print voxdim
        #print 'WARNING: assuming voxdim reverse of img.voxdim. Could be wrong'
        #mrixyz = (array([x,y,z]).T*voxdim).T

        #self.mrixyz = mrixyz
        #self.img = decimg
        #self.factor = dec
        #self.ind = array(nonz)
        #self.origimg = nim
        #self.data = decimg

if __name__ == "__main__":
    def __init__(self):
        self.nim=read()
        self.dec=decimate(self.nim, 5)

