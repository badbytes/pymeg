#  pdf2edf.py
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



#fname,data,n_samples_per_record,n_records,chlabels,srate,datetime,patient_name


'''Translate parts of pdf header to edf.'''
from misc import edfwrite
import copy
from numpy import floor,sqrt,tile
def convert(pdfinstance, patient_name, edf_filename):
    p = pdfinstance
    srate = p.data.srate
    patientid = p.data.pid
    fname = p.data.filepath
    frames = p.data.frames
    chlabels = copy.deepcopy(p.data.channels.labellist)
    scan = p.data.scan
    date_time = p.data.session
    data = p.data.data_block
    n_samples_per_record = floor(sqrt(p.data.frames))
    n_records = n_samples_per_record
    redata = data[0:n_samples_per_record*n_samples_per_record].T
    dt = date_time.replace('@_','').replace(':','@').replace('-','').replace('@','.')+'.00'
    dt = dt[3:6]+dt[0:2]+dt[5:]
    numr = tile(n_records,len(chlabels))
    record_length = frames / srate / n_records


    edfwrite.write_to_file(edf_filename,redata,numr.tolist(),n_records,chlabels, record_length,srate, dt,patientid,patient_name)
    #return fname,data,n_samples_per_record,n_records,chlabels,srate,datetime,patient_name
