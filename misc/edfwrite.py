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
from pdf2py import io_wrapper
fread = io_wrapper.fread

def write_edf_header(header, fname):
    h = header
    fid = open(fname, 'r')

    fid.write('0       ');

    # recording info)
    ind = fid.tell()
    fid.write(h['local_subject_id']);fid.seek(ind+80,0)
    fid.write(h['local_recording_id']);fid.seek(ind+80+80,0)

    # parse timestamp

    #(day, month, year) = [int(x) for x in re.findall('(\d+)', f.read(8))]
    #(hour, minute, sec)= [int(x) for x in re.findall('(\d+)', f.read(8))]
    #h['date_time']
    fid.write('10.12.0912.44.02')
    #h['date_time'] = str(datetime.datetime(year + 2000, month, day,
    #hour, minute, sec))

    # misc
    #header_nbytes = int(f.read(8))
    ind = fid.tell()
    fid.write(str(header_nbytes)); fid.seek(8+ind,0)
    #subtype = f.read(44)[:5]
    #h['EDF+'] = subtype in ['EDF+C', 'EDF+D']
    #h['contiguous'] = subtype != 'EDF+D'
    fid.write('EDF+C')#############################I THINK THIS MEANS CONTIN
    fid.seek(39)
    #h['n_records'] = int(f.read(8))
    print 'byte index', fid.tell()
    fid.write(str(numofsecondsinfile)) #Even though this is called n_records, it appers
    #to be the time in seconds in the file. 8bytes
    #h['record_length'] = float(f.read(8))  # in seconds
    fid.write('1')  # THIS also is weird, and not the length of file in seconds
    #nchannels = h['n_channels'] = int(f.read(4))
    fid.write(str(numberofchannels+1)) #dont know what the extra channel is for

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
    for i in chan_labels:
        ind = fid.tell()
        fid.write(i)
        fid.seek(16+ind,0)
    fid.seek(80,1) #skip 80bytes for transducer crap
    for i in arange(len(chan_labels)):
        fid.write('uV');fid.seek(8,1)
    fid.write('  ');fid.seek(8,1) #write units for the empty channel
    fid.write(str(min_data_val));fid.seek(16-len(min_data_val))
    

    #h['n_samples_per_record'] = [int(f.read(8)) for n in channels]
    fid.write(samplerate) #appears to be sample rate but called \
    #n_samples_per_record.
    f.read(32 * nchannels)  # reserved

    assert f.tell() == header_nbytes
    return h
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
'''
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

'''
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
