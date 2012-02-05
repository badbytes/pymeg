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
import os

EVENT_CHANNEL = 'EDF Annotations'

def write_edf_header(fname,nchannels,data):
    #h = header
    fid = open(fname, 'w')
    hdrbytes = 3328
    s = chararray(hdrbytes)
    s[:] = ' '
    s.tofile(fid)
    fid.seek(0)
    fid.write('0       ');

    # recording info)
    ind = fid.tell()
    chlabels = ['a','b','c','d','e','f','g','h','i','j','k']
    fid.write('X X X X');fid.seek(80-len('X X X X'),1)#fid.seek(ind+80,0)
    fid.write('Startdate 10-DEC-2009 X X test_generator');fid.seek(80-len('Startdate 10-DEC-2009 X X test_generator'),1)

    # parse timestamp

    #(day, month, year) = [int(x) for x in re.findall('(\d+)', f.read(8))]
    #(hour, minute, sec)= [int(x) for x in re.findall('(\d+)', f.read(8))]
    #h['date_time']
    fid.write('10.12.0912.44.02')
    fid.write(str(hdrbytes))

    #h['date_time'] = str(datetime.datetime(year + 2000, month, day,
    #hour, minute, sec))

    #!!NEED TO ADD ANNOTATIONS ChLabel
    EVENT_CHANNEL = 'EDF Annotations'
    print 'CL',chlabels
    #channel_labels = chlabels
    channel_labels = chlabels.append(EVENT_CHANNEL)
    print 'CL',chlabels
    # misc
    #header_nbytes = int(f.read(8))
    ind = fid.tell()
    ##fid.write(str(header_nbytes)); fid.seek(8+ind,0)
    #subtype = f.read(44)[:5]
    #h['EDF+'] = subtype in ['EDF+C', 'EDF+D']
    #h['contiguous'] = subtype != 'EDF+D'
    fid.seek(192)
    fid.write('EDF+C')#############################I THINK THIS MEANS CONTIN
    #fid.seek(39)
    fid.seek(236,0)
    #h['n_records'] = int(f.read(8))
    print 'byte index', fid.tell()
    numofsecondsinfile = 600
    fid.write(str(numofsecondsinfile)) #n_records...Even though this is called n_records, it appers
    #to be the time in seconds in the file. 8bytes
    #h['record_length'] = float(f.read(8))  # in seconds
    fid.seek(244)
    fid.write('1')  # record_length...THIS also is weird, and not the length of file in seconds
    #nchannels = h['n_channels'] = int(f.read(4))
    numberofchannels = 11
    fid.seek(252)
    fid.write(str(numberofchannels+1)) #Extra Channel is Annotations

    # read channel info
    '''channels = range(h['n_channels'])
    h['label'] = [f.read(16).strip() for n in channels]
    h['transducer_type'] = [f.read(80).strip() for n in channels]
    h['units'] = [f.read(8).strip() for n in channels]
    h['physical_min'] = np.asarray([float(f.read(8)) for n in channels])
    h['physical_max'] = np.asarray([float(f.read(8)) for n in channels])
    h['digital_min'] = np.asarray([float(f.read(8)) for n in channels])
    h['digital_max'] = np.asarray([float(f.read(8)) for n in channels])
    h['prefiltering'] = [f.read(80).strip() for n in channels]
    '''
    #write channel labels
    fid.seek(256)
    for i in chlabels:
        ind = fid.tell()
        fid.write(i)
        fid.seek(16+ind,0)
    #fid.write('EDF Annotations ');
    [fid.seek(80,1) for i in chlabels]#transducer_type skip 80bytes for transducer crap
    [fid.write('uV      ') for i in chlabels[:-1]]  #units
    fid.seek(8,1)
    #data[:] = float(1.2222222222)
    pmin = [];pmax = [];dmin=[];dmax=[]
    for i in data:
        pmin.append(float(min(i)))
        #array(str(float(min(i)))[:8]).tofile(fid) #Physical min
        array(['-1000.00']).tofile(fid)
    #fid.write('XX      ') #annotation min
    fid.write('-1      ') #annotation min
    for i in data:
        pmax.append(float(min(i)))
        #array(str(float(max(i)))[:8]).tofile(fid) #Physical max
        array(['1000.000']).tofile(fid)
    #fid.write('XX      ') #annotation min
    fid.write('1       ') #annotation max
    for i in data:
        dmin.append(float(min(i)))
        array(['-32768  ']).tofile(fid) #Digital max
    array(['-32768  ']).tofile(fid) #Digital max
    #array(str(float(min(i)))[:8]).tofile(fid) #Digital min
    #array([ -32767.,  -32767.,  -32767.,  -32767.,  -32767.,  -32767.,  -32767.\
    #,-32767.,  -32767.,  -32767.,  -32767.,  -32767.]).tofile(fid)
    #array([-32767.]).tofile(fid) #annotation min
    #fid.write('XX      ') #annotation min
    for i in data:
        dmax.append(float(max(i)))
        #array(str(float(max(i)))[:8]).tofile(fid) #Digital max
        array(['32767   ']).tofile(fid) #Digital max
        #array([ 32767.,  32767.,  32767.,  32767.,  32767.,  32767.,  32767.\
        #,32767.,  32767.,  32767.,  32767.,  32767.]).tofile(fid)
    array(['32767   ']).tofile(fid) #Digital max    #array([32767.]).tofile(fid) #annotation min
    #array(str(float(max(i)))[:8]).tofile(fid)
    #fid.write('XX      ') #annotation min

    [fid.seek(80,1) for i in chlabels] #prefiltering

    #h['n_samples_per_record'] = [int(f.read(8)) for n in channels]
    n_samples_per_record = [200,200,200,200,200,200,200,200,200,200,200,51]
    for n in n_samples_per_record:
        align(int(n),8,fid)
        #array(str(n)).tofile(fid)

    #[array(str(n)).tofile(fid) for n in n_samples_per_record]#appears to be sample rate but called n_samples_per_record.
    fid.seek(32 * nchannels)  # reserved

    #assert f.tell() == header_nbytes
    #return h
    #fid.close()

    # calculate ranges for rescaling
    dig_min = array([dmin])
    phys_min = array([pmin])
    phys_range = array([pmax]) - array([pmin])
    dig_range = array([dmax]) - array([dmin])
    #assert all(phys_range > 0)
    #assert all(dig_range > 0)
    gain = phys_range / dig_range

    range_scale = {'dmin':dig_min,'pmin':phys_min,'prange':phys_range,'drange':dig_range,'gain':gain}
    print 'RANGE',range_scale
    n_records = numofsecondsinfile
    return fid, n_records, data, range_scale, n_samples_per_record, chlabels

    #(200*11*600+(600*51))*2 +++ 3328

def align(val,fieldsize,fid): #string to write and size of field to skip
    curind = fid.tell()
    print val
    array(str(val)).tofile(fid)
    v = str(float(val))
    print 'V',v,'x ',curind,'y',fieldsize
    fid.seek(curind+fieldsize)

def write_data(fid,data,n_records,range_scale, n_samples_per_record, chlabels):
    #fid.seek(os.SEEK_END)
    scaleddata = (data + range_scale['dmin'].T) / range_scale['gain'].T - range_scale['pmin'].T
    redata = scaleddata.reshape(size(scaleddata,0),size(scaleddata,1)/n_records,n_records) #CH,Epoch,Samples
    print redata.shape, 'SHAPE',n_records, n_samples_per_record, chlabels
    #redata[0,:,1].tofile(fid);return
    for samp in arange(n_records): #For each epoch
        #for nsamp in n_samples_per_record: #arange(n_records): #For each sample in epoch
        for chan in chlabels: #For each channel
            #scaledj = (redata[:,i]+range_scale['dmin'][j]) / range_scale['gain'][j] - range_scale['pmin']
            cnum = chlabels.index(chan)
            print cnum, samp, chan
            if chan == EVENT_CHANNEL:
                fid.seek(n_samples_per_record[cnum],1)
            else:
                redata[cnum,:,samp].tofile(fid)
    fid.close()


    #for (i, samples) in enumerate(raw_record):
      #if h['label'][i] == EVENT_CHANNEL:
        #ann = tal(samples)
        #time = ann[0][0]
        #events.extend(ann[1:])
      #else:
        ## 2-byte little-endian integers
        #dig = np.fromstring(samples, '<i2').astype(float)
        #phys = (dig - dig_min[i]) * gain[i] + phys_min[i]
        #signals.append(phys)

    #fromstring(d[5],'<i2').astype(float)

def write_to_file(fname,nchan,data):
    '''test_'''
    fid, n_records, data, range_scale, n_samples_per_record, chlabels = write_edf_header(fname,nchan,data)

    write_data(fid,data,n_records, range_scale, n_samples_per_record, chlabels)


'''def edf_header(f):
  h = {}
  assert f.tell() == 0  # check file position
  assert f.read(8) == '0       '

  # recording info)
  h['local_subject_id'] = f.read(80).strip()
  h['local_recording_id'] = f.read(80).strip()

  # parse timestamp
  (day, month, year) = [int(x) for x in re.findall('(\d+)', f.read(8))]
  (hour, minute, sec)= [int(x) for x in re.findall('(\d+)', f.read(8))]
  h['date_time'] = str(datetime.datetime(year + 2000, month, day,
    hour, minute, sec))

  # misc
  header_nbytes = int(f.read(8))
  subtype = f.read(44)[:5]
  h['EDF+'] = subtype in ['EDF+C', 'EDF+D']
  h['contiguous'] = subtype != 'EDF+D'
  h['n_records'] = int(f.read(8))
  h['record_length'] = float(f.read(8))  # in seconds
  nchannels = h['n_channels'] = int(f.read(4))

  # read channel info
  channels = range(h['n_channels'])
  h['label'] = [f.read(16).strip() for n in channels]
  h['transducer_type'] = [f.read(80).strip() for n in channels]
  h['units'] = [f.read(8).strip() for n in channels]
  h['physical_min'] = np.asarray([float(f.read(8)) for n in channels])
  h['physical_max'] = np.asarray([float(f.read(8)) for n in channels])
  h['digital_min'] = np.asarray([float(f.read(8)) for n in channels])
  h['digital_max'] = np.asarray([float(f.read(8)) for n in channels])
  h['prefiltering'] = [f.read(80).strip() for n in channels]
  h['n_samples_per_record'] = [int(f.read(8)) for n in channels]
  f.read(32 * nchannels)  # reserved

  assert f.tell() == header_nbytes
  return h

HEADER RECORD
8 ascii : version of this data format (0)
80 ascii : local patient identification
80 ascii : local recording identification
8 ascii : startdate of recording (dd.mm.yy)
8 ascii : starttime of recording (hh.mm.ss)
8 ascii : number of bytes in header record
44 ascii : reserved
8 ascii : number of data records (-1 if unknown)
8 ascii : duration of a data record, in seconds
4 ascii : number of signals (ns) in data record
ns * 16 ascii : ns * label (e.g. EEG FpzCz or Body temp)
ns * 80 ascii : ns * transducer type (e.g. AgAgCl electrode)
ns * 8 ascii : ns * physical dimension (e.g. uV or degreeC)
ns * 8 ascii : ns * physical minimum (e.g. -500 or 34)
ns * 8 ascii : ns * physical maximum (e.g. 500 or 40)
ns * 8 ascii : ns * digital minimum (e.g. -2048)
ns * 8 ascii : ns * digital maximum (e.g. 2047)
ns * 80 ascii : ns * prefiltering (e.g. HP:0.1Hz LP:75Hz)
ns * 8 ascii : ns * nr of samples in each data record
ns * 32 ascii : ns * reserved

DATA RECORD
nr of samples[1] * integer : first signal in the data record
nr of samples[2] * integer : second signal
..
..
nr of samples[ns] * integer : last signal


clear()
name = xgetfile('*.*')                          // name of file
printf ("File selected : %s",name);             // file selected
fid = mopen (name,'rb');                        // opens file
mseek(0,fid,'end');                             // goes to the end
totalbytes = mtell(fid);                        // reads bytes
mseek(0,fid)                                    // goes beginning
header = mgetstr (256, fid);                    // reads header
version = part (header, 1:8);                   // version
patientid = part (header, 9:88);                // patient ident.
recordid = part (header, 89:166);               // record ident.
startdate = part (header, 169:176);             // date
starttime = part (header, 177:184);             // time
nbytesheader = eval (part (header, 185:192));   // bytes of header
reserved = part (header , 193:236);             // reserved field
ndatarecords = eval ( part (header, 237:244));  // data records
duration = eval ( part (header, 245:252));      // duration
nsignals = eval ( part (header, 253:256));      // number of sign.'''