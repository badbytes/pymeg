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
mr = pydicom.read(pathtodicom, prefix='MR')'''

import dicom
import os
import subprocess
import time
from numpy import size, shape, zeros, int16, int8, append, array, argsort, random

def uncompress(pathtodicom,file):
    s = subprocess.Popen('dcmdjpeg '+pathtodicom+'/'+file+' /tmp/'+'un_'+file, shell=True,stdout=True)
    print 'uncompressing file to /tmp/un_'+file
    time.sleep(.25) #need to sleep to give time to write the file
    dicomfile = dicom.ReadFile('/tmp/'+'un_'+file)
    return dicomfile

def build3d(data):
    pass


class read:
    def __init__(self, pathtodicom, prefix):
        '''mr = pydicom.read(pathtodicom, prefix='MR')'''

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

        self.sampleheader = dicomfile

        #build array of data
        self.seqdict = {}
        self.fndict = {}
        self.seqind = {}
        self.arrayshape = {}
        self.sliceloc = {}
        self.pathtodicom = pathtodicom
        self.pixdim = {}
        self.imageorientation = {}
        self.SeriesInstanceUID = {}
        self.MediaStorageSOPInstanceUID = {}

        for i in range(0, size(files)):
            #try:
                #print(dicomfile.SliceLocation)
            #except AttributeError:


            dicomfile = dicom.ReadFile(pathtodicom+'/'+files[i])
            try: #check compression
                comp = 'no'
                dicomfile.PixelArray
            except NotImplementedError: #uncompress
                comp = 'yes'
                dicomfile = uncompress(pathtodicom, files[i])

            try:
                self.seqdict[dicomfile.SeriesTime]
            except AttributeError:
                print(dicomfile)
            except KeyError:
                self.seqdict[dicomfile.SeriesTime] = array([])
                self.fndict[dicomfile.SeriesTime] = []
                self.seqind[dicomfile.SeriesTime] = []
                self.sliceloc[dicomfile.SeriesTime] = []
                try:
                    self.imageorientation[dicomfile.SeriesTime] = dicomfile.ImageOrientationPatient
                    self.pixdim[dicomfile.SeriesTime] = array([dicomfile.PixelSpacing[0],dicomfile.PixelSpacing[1],dicomfile.SliceThickness])
                except AttributeError:
                    pass #perhaps functional data
                self.arrayshape[dicomfile.SeriesTime] = [size(dicomfile.PixelArray,0),size(dicomfile.PixelArray,1)]#dicomfile.AcquisitionMatrix[1:3]
                self.SeriesInstanceUID[dicomfile.SeriesTime] = [] #dicomfile.SeriesInstanceUID
                self.MediaStorageSOPInstanceUID[dicomfile.SeriesTime] = []

            #try:

                #print(i, dicomfile.AcquisitionNumber,dicomfile.InstanceNumber, \
                #dicomfile.SeriesNumber, dicomfile.ProtocolName,\
                #dicomfile.SliceLocation,dicomfile.SeriesTime)
            #except AttributeError:
                #pass #perhaps functional data
            print(i, dicomfile.AcquisitionNumber,dicomfile.InstanceNumber, \
            dicomfile.SeriesNumber, dicomfile.SeriesDescription)




            self.seqdict[dicomfile.SeriesTime] = append(self.seqdict[dicomfile.SeriesTime], dicomfile.PixelArray)
            if comp == 'yes':
                prefix = 'un_'
            else:
                prefix = ''
            self.fndict[dicomfile.SeriesTime].append(prefix+files[i])
            self.seqind[dicomfile.SeriesTime].append(dicomfile.InstanceNumber-1)
            try:
                self.sliceloc[dicomfile.SeriesTime].append(dicomfile.SliceLocation)
            except AttributeError:
                self.sliceloc[dicomfile.SeriesTime].append(dicomfile.InstanceNumber)
            self.SeriesInstanceUID[dicomfile.SeriesTime].append(str(dicomfile.SeriesInstanceUID))
            self.MediaStorageSOPInstanceUID[dicomfile.SeriesTime].append(str(dicomfile.MediaStorageSOPInstanceUID))

        #reshape it to 3d and order slices based on location
        self.sortslice = {}
        for f in range(0, len(self.sliceloc)):
            self.sortslice[self.sliceloc.keys()[f]] = argsort(self.sliceloc[self.sliceloc.keys()[f]])

        print(self.sortslice)
        #return
        self.datareshaped = {}
        for e in range(0, len(self.sortslice)): #for each series
            print 'sorting dataset',e
            seqID = self.seqdict.keys()[e]
            print(seqID, self.seqdict[seqID].shape)
            self.datareshaped[seqID] = self.seqdict[seqID].reshape(len(self.seqind[seqID]),self.arrayshape[seqID][0],self.arrayshape[seqID][1])
            print shape(self.datareshaped[seqID])

            self.datareshaped[seqID] = self.datareshaped[seqID][self.sortslice[seqID]]
            self.fndict[seqID] = array(self.fndict[seqID])[self.sortslice[seqID]]
            self.seqind[seqID] = array(self.seqind[seqID])[self.sortslice[seqID]]
            self.sliceloc[seqID] = array(self.sliceloc[seqID])[self.sortslice[seqID]]


            slicediff = self.sliceloc[seqID][1]-self.sliceloc[seqID][0]
            if (slicediff - dicomfile.SliceThickness) > .01:
                print 'adjacent slice location',slicediff, 'differs from Slice Thickness',dicomfile.SliceThickness,' as reported in file. Using inter-slice thickness as slice thickness for header.'
                self.pixdim[seqID][2] = slicediff
            else:
                print 'adjacent slice location',slicediff, 'close to Slice Thickness',dicomfile.SliceThickness,' as reported in file. Using header slice thickness.'


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

