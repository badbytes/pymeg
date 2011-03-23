#       pydicom.py
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



'''read and write dicom series
mr = pydicom.loadfiles(pathtodicom, prefix='MR')
mr.__importfiles() #reads associated dicom files
mr.__createarray__() #builds array of images. 3D

#OR
mr = pydicom.loadfiles(pathtodicom, prefix=fileprefixstring)
mr.dicom2nifti() #does all


'''

import dicom
import os
import subprocess
import time
from numpy import size, shape, zeros, int16, int8, append, array, argsort, random, frombuffer, squeeze

def uncompress(pathtodicom,file):
    s = subprocess.Popen('dcmdjpeg '+pathtodicom+'/'+file+' /tmp/'+'un_'+file, shell=True,stdout=True)
    print 'uncompressing file to /tmp/un_'+file
    while os.path.exists('/tmp/'+'/'+'un_'+file) == False:
        time.sleep(.1)

    while s.poll() != 0:
        print('waiting for file decompression to finish')
        time.sleep(.1)

    dicomfile = dicom.ReadFile('/tmp/'+'un_'+file)

    return dicomfile

def build3d(data):
    pass


class loadfiles:

    def __init__(self, pathtodicom, prefix):
        '''mr = pydicom.read(pathtodicom, prefix='MR')'''
        self.pathtodicom = pathtodicom
        self.prefix = prefix

        path = os.walk(pathtodicom)
        files = path.next()[2]
        files.sort()

        filesMR = []
        for f in files:
            if f.startswith(prefix) == True:
                filesMR.append(f)
            else:
                print 'found file without selected prefix', f

        files = filesMR

        #make emtpy array
        try:
            dicomfile = dicom.ReadFile(pathtodicom+'/'+files[0]) #read 1st file
        except IndexError:
            print 'you probably have the wrong prefix option. prefix="MR"'
            print 'try again'
            return
        self.files = files
        self.pathtodicom = pathtodicom
        return

    def __dicomread__(self, i):
        '''load data from filelist and uncompress if necessary'''
        dicomfile = dicom.ReadFile(self.pathtodicom+'/'+i)
        try: #check compression
            comp = 'no'
            b = dicomfile.PixelArray
        except NotImplementedError: #uncompress
            comp = 'yes'
            #b = frombuffer(j.PixelArray, dtype='uint8')
            dicomfile = uncompress(self.pathtodicom, i)
        return dicomfile


    def __importfiles__(self):
        d = array([])
        for i in self.files:
            #dicomfile = dicom.ReadFile(self.pathtodicom+'/'+i)
            print('reading',i)
            dicomfile = self.__dicomread__(i)
            #try: #check compression
                #comp = 'no'
                #b = dicomfile.PixelArray
            #except NotImplementedError: #uncompress
                #comp = 'yes'
                ##b = frombuffer(j.PixelArray, dtype='uint8')
                #dicomfile = uncompress(self.pathtodicom, i)
            d = append(d,dicomfile)
        self.dicomdict = {dicomfile.SeriesTime : d}
        return

    def __rename__(self, writepath=None, descriptor_field=None, slice_field=None, extra_field=None):

        if writepath == None:
            print('no path given. exiting')
            return
        if writepath[-1] != '/':
            writepath = writepath+'/'
        if os.path.exists(writepath) == False:
            print 'something wrong with your path. try again'
            return

        if descriptor_field == None:
            df = 'SeriesDescription' #default
        if slice_field == None:
            sf = 'InstanceNumber' #default

        self.d = array([])
        for i in self.files:
            dicomfile = self.__dicomread__(i)

            try:
                filename_descriptor = str(eval(('dicomfile.'+df))).replace(' ','')
            except AttributeError:
                time.sleep(1.5)
                #self.tmp = dicomfile
                dicomfile = self.__dicomread__(i)
                filename_descriptor = str(eval(('dicomfile.'+df))).replace(' ','')
            filename_slice = str(eval(('dicomfile.'+sf))).replace(' ','')
            filename_rowscolumns = str(dicomfile.Rows)+'X'+str(dicomfile.Columns)
            sid = str(dicomfile.SeriesInstanceUID)#.split('.')[-1])
            fn = writepath+filename_descriptor+'_'+sid+'_'+filename_slice+'_'+filename_rowscolumns
            #if os.path.exists(fn+'.dcm') == True:
                #fn = fn+'B'
            fn = fn+'.dcm'
            print('saving',fn)
            #if filename_descriptor == 'SegStructuralMentalRhyming':
            self.d = append(self.d, i+filename_descriptor)
            dicomfile.SaveAs(fn)

    def __createarray__(self):
        '''build dictionary result arrays of slices from dicom series'''
        self.arraydict = {}; self.reshapedarraydict = {};
        for i in self.dicomdict.keys(): #for each series
            print('building',i)
            slicearray = []
            for j in self.dicomdict[i]: #for each slice
                try:
                    if sum(sdim-sdim) != 0: #check and make sure the pixel dims are exact
                        print('pixel dims dont match from slice to slice. exiting')
                        return
                except NameError:
                    sdim = array([j.SamplesperPixel,j.Columns,j.Rows])
                    print sdim
                slice = j.PixelArray
                slicearray = append(slicearray,slice)
                sdim = array([j.SamplesperPixel,j.Columns, j.Rows])
            self.arraydict[i] = slicearray
            numofslices = len(self.arraydict[i])/sdim[0]/sdim[1]/sdim[2]
            print('numofslices', numofslices)
            self.reshapedarraydict[i] = self.arraydict[i].reshape((sdim[0],sdim[1],sdim[2],numofslices), order='F')

        return

    def __niftiinfo__(self):
        self.pixdim = {}
        self.imageorientation = {}
        self.datareshaped = {}
        for i in self.dicomdict.keys():
            for j in self.dicomdict[i]:
                try:
                    if (self.ImageOrientation == j.ImageOrientationPatient) == False:
                        print('mismatch in image orientation. image irregularity. exiting')
                        print('image #',instancenum,'orientation',self.ImageOrientation)
                        print('image #',j.InstanceNumber,'orientation',j.ImageOrientationPatient)
                        return -1
                    if (self.PixelSpacing == j.PixelSpacing) == False:
                        print('image #',instancenum,'pixdim',self.PixelSpacing)
                        print('image #',j.InstanceNumber,'orientation',j.PixelSpacing)
                    if (self.SliceThickness == j.SliceThickness) == False:
                        print('image #',instancenum,'pixdim',self.SliceThickness)
                        print('image #',j.InstanceNumber,'orientation',j.SliceThickness)

                except AttributeError: pass #first iter of loop
                self.ImageOrientation = j.ImageOrientationPatient
                self.PixelSpacing = j.PixelSpacing
                self.SliceThickness = j.SliceThickness

                instancenum = j.InstanceNumber

            self.pixdim[i] = append(self.PixelSpacing,self.SliceThickness)
            self.imageorientation[i] = self.ImageOrientation
            self.datareshaped[i] = squeeze(self.reshapedarraydict[i]).T
        self.seqdict = self.arraydict

    def dicom2nifti(self):
        '''calls several functions to read, import, build array and get nifti info from dicom series'''
        #self.__read__(self.pathtodicom,self.prefix)
        self.__importfiles__()
        self.__createarray__()
        self.__niftiinfo__()

class write:
    def __init__(self, dicom_instance, seqID, data, savename=None, studydate='', studytime=''):

        headernew = {'Manufacturer':'4D', 'InstitutionName':'UCdenver', 'ReferringPhysiciansName':'NA', 'StationName':'', \
         'StudyDescription':'MEG', 'SeriesDescription':'Density', \
        'OperatorsName':'DC', 'ManufacturersModelName':'BTI', 'SoftwareVersions':'', 'ProtocolName':'',\
        'StudyDate':studydate, 'SeriesDate':studydate,  'AcquisitionDate':studydate , 'ContentDate':studydate, \
        'StudyTime':studytime,'SeriesTime':studytime,'AcquisitionTime':studytime, 'ContentTime':studytime, 'Modality':'MEG', \
        'NameofPhysiciansReadingStudy':'mlr',  }
        UIDrand = int(random.rand()*100)

        '''
        headernewdate='20091117', time='110600', Manufacturer='4D', InstitutionName='UCdenver', ReferringPhysiciansName='NA', StationName='', StudyDescription='MEG', SeriesDescription='SEF'
        OperatorsName'DC', ManufacturersModelName='BTI', SoftwareVersions='', ProtocolName=''

        '''
        '''seqID = '131847.875000' '''
        '''145611'''

        if savename == None:
            savename = 'dd'

        path = os.walk(dicom_instance.pathtodicom)
        filesindir = path.next()[2]
        filesindir.sort()


        filelist = dicom_instance.fndict[seqID]
        fnlist = dicom_instance.fndict[seqID].tolist()

        for f in filelist:
            self.fnlist = fnlist
            self.f = f

            try:
                ind = filesindir.index(f)
                print ind
            except ValueError:
                pass #not in file list...skip
                print 'cant find file, skipping', f
            else:
                print 'writing image', f, savename
                dicomfile = dicom.ReadFile(dicom_instance.pathtodicom+'/'+filesindir[ind])
                if dicomfile.BitsAllocated == 16:
                    data = int16(data)
                if dicomfile.BitsAllocated == 8:
                    data = int8(data)

                #modify header
                for h in headernew:
                    setattr(dicomfile,h,headernew[h])
                    SIUlast = dicomfile.SeriesInstanceUID.split('.')[-1]
                    SIUlen = len(SIUlast)
                    dicomfile.SeriesInstanceUID=dicomfile.SeriesInstanceUID[:-int(SIUlen):]+str(int(SIUlast)+1000+UIDrand)
                    MSUlast = dicomfile.MediaStorageSOPInstanceUID.split('.')[-1]
                    MSUlen = len(MSUlast)
                    dicomfile.MediaStorageSOPInstanceUID=dicomfile.MediaStorageSOPInstanceUID[:-int(MSUlen):]+str(int(MSUlast)+1000+UIDrand)
                    SOPlast = dicomfile.SOPInstanceUID.split('.')[-1]
                    SOPlen = len(SOPlast)
                    dicomfile.SOPInstanceUID=dicomfile.SOPInstanceUID[:-int(SOPlen):]+str(int(SOPlast)+1000+UIDrand)

                print dicomfile.MediaStorageSOPInstanceUID, dicomfile.SOPInstanceUID
                print 'dataslice', fnlist.index(f) #dicom_instance.fndict[seqID].index(f)
                dicomfile.PixelData = data[:,:,fnlist.index(f)].tostring()#data[fnlist.index(f),:,:].tostring()
                fnamestripped = os.path.splitext(f)[0]
                #dicomfile.SaveAs(dicom_instance.pathtodicom+'/'+fnamestripped+'_'+savename+'.dcm')
                dicomfile.SaveAs(dicom_instance.pathtodicom+fnamestripped+'_'+savename+'.dcm')


"""Routines for viewing DICOM image data

"""
# Copyright (c) 2008 Darcy Mason
# This file is part of pydicom, relased under an MIT license.
#    See the file license.txt included with this distribution, also
#    available at http://pydicom.googlecode.com

have_PIL=True
try:
    import PIL.Image
except:
    have_PIL = False

# Display an image using the Python Imaging Library (PIL)
def show_PIL(dataset):
    if not have_PIL:
        raise ImportError, "Python Imaging Library is not available. See http://www.pythonware.com/products/pil/ to download and install"
    if 'PixelData' not in dataset:
        raise TypeError, "Cannot show image -- DICOM dataset does not have pixel data"

    # Map BitsAllocated and SamplesperPixel to PIL's "mode"
    # PIL mode info from http://www.pythonware.com/library/pil/handbook/concepts.htm
    bits = dataset.BitsAllocated
    samples = dataset.SamplesperPixel
    if bits == 8 and samples == 1:
        mode = "L"
    elif bits == 8 and samples == 3:
        mode = "RGB"
    elif bits == 16:
        mode = "I;16" # not sure about this -- PIL source says is 'experimental' and no documentation. Also, should bytes swap depedning on endian of file and system??
    else:
        raise TypeError, "Don't know PIL mode for %d BitsAllocated and %d SamplesPerPixel" % (bits, samples)

    # PIL size = (width, height)
    size = (dataset.Columns, dataset.Rows)

    im = PIL.Image.frombuffer(mode, size, dataset.PixelData, "raw", mode, 0, 1) # Recommended to specifiy all details by http://www.pythonware.com/library/pil/handbook/image.htm
    im.show()


if __name__ == '__main__':
    r = read(pathtodicom, prefix=None)
    pathtodicom = '/home/danc/data/brains/0097'
    pathtodicom = '/home/danc/python/data/clinicaltests/E-0031MRI/sub'
    mrdata = mr.seqdict[mr.seqdict.keys()[2]]
    viewmri.display(fliplr(mrdata.swapaxes(2,0).swapaxes(1,2)))
    #from mri import pydicom


