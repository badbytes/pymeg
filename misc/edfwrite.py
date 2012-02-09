#  edfwrite.py
#
#  Copyright 2012 dan collins <danc@badbytes.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#from pdf2py import io_wrapper
#fread = io_wrapper.fread
#fwrite = io_wrapper.fwrite

from numpy import *
import os, logging, datetime

logger = logging.getLogger('1')
logger.addHandler(logging.FileHandler('/tmp/logger.write',mode='w'))

class DataChannelMismatch:
    pass #print 'Data and Channel numbers dont match'

EVENT_CHANNEL = 'EDF Annotations'
#edfwrite.write_to_file('/tmp/test.edf', 17,d,numr.tolist(),1,eeglabs)
#l = ['FP1','F7','T3','T5','01','F3','C3','P3','FZ','CZ','PZ','FP2','F4','C4','P4','02','F8','T4','T6']
#p = pdf.read(f[0]);p.data.setchannellabels(eeglabs);p.data.getdata(0,15000)
#edfwrite.write_to_file('/tmp/test.edf',19,d.T,numr.tolist(),30,l)

#edfwrite.write_to_file('/tmp/test.edf',19,d.T,numr.tolist(),150,l)

def write_edf_header(fname,data,n_samples_per_record,n_records,chlabels,srate,date_time,patient_id,patient_name,record_length):
    '''n_samples_per_record = [200,200,200,200,200,200,200,200,200,200,200,51]
    chlabels = ['a','b','c','d','e','f','g','h','i','j','k']
    n_records = 600 #number of samples per epoch. Must be more than one epoch, so reshape to 3D data as necessary
    srate = samples per sec
    datetime = dd.mm.yy.hh.mm.ss
    patient_name = D_C
    record_length is the time in sec for length of epoch
    '''
    #h = header
    fid = open(fname, 'w')
    nchannels = len(chlabels)

    #make data Channel X Time
    print 'CHlabels', chlabels
    if len(chlabels) == size(data,0):
        pass
    elif len(chlabels) == size(data,1):
        data = data.T
        #print 'numch:',len(chlabels),'sizeofdata:',shape(data)
    else:
        print 'Data and Channels dont match', 'numch:',len(chlabels),'sizeofdata:',shape(data)
        raise DataChannelMismatch

    #data = data[:,floor(sqrt(data.shape))[1]] #round down for easy reshaping

    numch = len(chlabels)+1; #Add a Annotation channel
    print 'NumofCh',numch
    edfformat = {'version': 8, 'patid':80, 'recid':80,'date':8,'time':8,'numbytes':8, \
    'res':44,'n_records':8,'rec_dur':8,'num_rec':4,'labels':numch*16, \
    'trasducer':numch*80, 'units':numch*8,'pmin':numch*8, 'pmax':numch*8, \
    'dmin':numch*8, 'dmax':numch*8,'prefilt':numch*80,'num_samp': numch*8, 'reserved': numch*32}
    hdrbytes = sum(edfformat.values())

    # not sure if necessary, but create whitespace for header
    s = chararray(hdrbytes)
    s[:] = ' '
    s.tofile(fid)

    fid.seek(0) #Jump to start of file

    fid.write('0       '); #Data Version
    ind = fid.tell()

    #patient/recording info
    patientinfo = str(patient_id+' X X '+patient_name) #PatientID, Sex, DOB, Last_First name
    align(patientinfo,80,fid) #fid.write(patientinfo); #PatientID, Sex, DOB, Last_First name
    #fid.seek(80-len(patientinfo),1)#fid.seek(ind+80,0)

    year = int('20'+date_time[6:8])
    month = int(date_time[0:2])
    day = int(date_time[3:5])
    hour = int(date_time[8:10])
    minute = int(date_time[11:13])
    second = int(date_time[14:16])
    dt = datetime.datetime(year,month,day,hour,minute,second)
    monthabb = dt.strftime('%B')[0:3].upper()
    scaninfo = str('Startdate '+date_time[3:5]+'-'+monthabb+'-'+str(year)+' X X Neuroimaging_UCD') #'Startdate 10-DEC-2009 X X test_generator'
    align(scaninfo,80,fid) #fid.write(scaninfo);fid.seek(80-len(scaninfo),1)

    # parse timestamp
    fid.write(date_time) #'10.12.0912.44.02')
    fid.write(str(hdrbytes))

    #!!NEED TO ADD ANNOTATIONS ChLabel
    EVENT_CHANNEL = 'EDF Annotations'
    print 'CL',chlabels
    chlabels.append(EVENT_CHANNEL)
    n_samples_per_record.append(51)
    print 'CL',chlabels
    ind = fid.tell()
    fid.seek(192)
    fid.write('EDF+C')#############################I THINK THIS MEANS CONTIN

    fid.seek(236,0)
    print 'byte index', fid.tell()
    fid.write(str(int(n_records))) #
    fid.seek(244)

    fid.write(str(record_length)[:8])#'0.344068') #This is numsamplesindata / srate / n_records  # record_length
    fid.seek(252)
    fid.write(str(numch)) #Extra Channel is Annotations
    #write channel labels
    fid.seek(256)
    for i in chlabels:
        ind = fid.tell()
        fid.write(i)
        fid.seek(16+ind,0)
    [fid.seek(80,1) for i in chlabels]#transducer_type
    [fid.write('uV      ') for i in chlabels[:-1]]  #units
    fid.seek(8,1)

    #Max and Mins
    pmin = [];pmax = [];dmin=[];dmax=[]
    for i in data:
        pmin.append(-1000.)
        array(['-1000.00']).tofile(fid)
    fid.write('-1      ') #annotation min
    for i in data:
        pmax.append(1000.)
        array(['1000.000']).tofile(fid)
    fid.write('1       ') #annotation max
    for i in data:
        dmin.append(-32767.)
        array(['-32768  ']).tofile(fid) #Digital max
    array(['-32768  ']).tofile(fid) #Digital max
    for i in data:
        dmax.append(32767.)
        array(['32767   ']).tofile(fid) #Digital max
    array(['32767   ']).tofile(fid) #Digital max    #array([32767.]).tofile(fid) #annotation min

    [fid.seek(80,1) for i in chlabels] #prefiltering
    for n in n_samples_per_record:
        align(int(n),8,fid)
    print 'DEBUG END OF HEADER',fid.tell()

    #[array(str(n)).tofile(fid) for n in n_samples_per_record]#appears to be sample rate but called n_samples_per_record.
    fid.seek(32 * nchannels,1)  # reserved
    print 'DEBUG END OF HEADER',fid.tell()
    header_nbytes = fid.tell()# == header_nbytes

    # calculate ranges for rescaling
    dig_min = array([dmin])
    phys_min = array([pmin])
    phys_range = array([pmax]) - array([pmin])
    dig_range = array([dmax]) - array([dmin])
    gain = phys_range / dig_range

    range_scale = {'dmin':dig_min,'pmin':phys_min,'prange':phys_range,'drange':dig_range,'gain':gain}
    print 'RANGE',range_scale
    #n_records = n_records
    return fid, n_records, data, range_scale, n_samples_per_record, chlabels

    #(200*11*600+(600*51))*2 +++ 3328

def align(val,fieldsize,fid): #string to write and size of field to skip
    curind = fid.tell()
    print val
    array(str(val)).tofile(fid)
    #v = str(float(val))
    #print 'V',v,'x ',curind,'y',fieldsize
    fid.seek(curind+fieldsize)

def write_data(fid,data,n_records,range_scale, n_samples_per_record, chlabels):
    fid.seek(0,2);
    print 'DATA START',fid.tell(), shape(data),n_records
    scaleddata = data# + range_scale['dmin'].T) / range_scale['gain'].T - range_scale['pmin'].T
    redata = squeeze(scaleddata.reshape(size(scaleddata,0),size(scaleddata,1)/n_records,n_records, order='F'))
    print redata.shape, 'SHAPE',n_records, n_samples_per_record, chlabels, fid.tell()
    ind = 0
    for samp in arange(n_records): #For each epoch
        string_zeros = ''
        zlength = 102 - 1 - len(str(ind)) - 2 #annotation is length of 51 minus space for '+' minus 2 'x14' seperators, minus the length of the sample 'ind'
        for i in arange(zlength):
            string_zeros = string_zeros+'\x00'
        for chan in chlabels: #For each channel
            cnum = chlabels.index(chan)
            nsamp = n_samples_per_record[chlabels.index(chan)]
            if chan == EVENT_CHANNEL:
                ann = '+'+str(ind)+'\x14\x14'+string_zeros #\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                fid.write(ann)
                ind = ind+1
            else:
                redata[cnum,:,samp].astype(int16).tofile(fid)
                #redata[cnum,samp].astype(int16).tofile(fid)
    fid.close()

def write_to_file(fname,data,n_samples_per_record,n_records,chlabels,record_length,srate,datetime,patient_id,patient_name):
    #edf_filename,data,numr.tolist(),n_records,chlabels, record_length
    fid, n_records, data, range_scale, n_samples_per_record, chlabels = write_edf_header(fname,data,n_samples_per_record,n_records,chlabels,srate,datetime,patient_id,patient_name,record_length)
    write_data(fid,data,n_records, range_scale, n_samples_per_record, chlabels)
    #return r,x

#'+0\x14\x14\x00+0.0000\x14RECORD START\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#'+4\x14\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

