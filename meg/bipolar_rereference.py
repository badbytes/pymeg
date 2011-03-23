#       bipolar_rereference.py
#       
#       Copyright 2009 dan collins <danc@badbytes.net>
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


'''bipolar_rereference

eeg = pdf.read(fn[0])
eeg.data.setchannels('eeg')
eeg.data.getdata(0,p.data.pnts_in_file, eeg.data.channels.channelsind)
eeg.data.channels.channelsname
'''



from numpy import zeros, shape, where, size


def eeg(data, chlabels):
    '''d,l = bipolar_rereference.eeg(eeg.data.data_block, eeg.data.channels.channelsname)'''
    z = zeros((size(data,0),19))
    
    z[:,0] = data[:,where(chlabels == 'FP1')[0][0]] - data[:,where(chlabels == 'F3')[0][0]]
    z[:,1] = data[:,where(chlabels == 'F3')[0][0]] - data[:,where(chlabels == 'C3')[0][0]]
    z[:,2] = data[:,where(chlabels == 'C3')[0][0]] - data[:,where(chlabels == 'P3')[0][0]]
    z[:,3] = data[:,where(chlabels == 'P3')[0][0]] - data[:,where(chlabels == '01')[0][0]]
    z[:,4] = data[:,where(chlabels == 'FP1')[0][0]] - data[:,where(chlabels == 'F7')[0][0]]
    z[:,5] = data[:,where(chlabels == 'F7')[0][0]] - data[:,where(chlabels == 'T3')[0][0]]
    z[:,6] = data[:,where(chlabels == 'T3')[0][0]] - data[:,where(chlabels == 'T5')[0][0]]
    z[:,7] = data[:,where(chlabels == 'T5')[0][0]] - data[:,where(chlabels == '01')[0][0]]
    z[:,8] = data[:,where(chlabels == 'FP2')[0][0]] - data[:,where(chlabels == 'F4')[0][0]]
    z[:,9] = data[:,where(chlabels == 'F4')[0][0]] - data[:,where(chlabels == 'C4')[0][0]]
    z[:,10] = data[:,where(chlabels == 'C4')[0][0]] - data[:,where(chlabels == 'P4')[0][0]]
    z[:,11] = data[:,where(chlabels == 'P4')[0][0]] - data[:,where(chlabels == '02')[0][0]]
    z[:,12] = data[:,where(chlabels == 'FP2')[0][0]] - data[:,where(chlabels == 'F8')[0][0]]
    z[:,13] = data[:,where(chlabels == 'F8')[0][0]] - data[:,where(chlabels == 'T4')[0][0]]
    z[:,14] = data[:,where(chlabels == 'T4')[0][0]] - data[:,where(chlabels == 'T6')[0][0]]
    z[:,15] = data[:,where(chlabels == 'T6')[0][0]] - data[:,where(chlabels == '02')[0][0]]
    z[:,16] = data[:,where(chlabels == 'VEOG')[0][0]]
    z[:,17] = data[:,where(chlabels == 'HEOG')[0][0]]
    z[:,18] = data[:,where(chlabels == 'EKG')[0][0]]


    
    
    labels = ['FP1-F3', 'F3-C3', 'C3-P3', 'P3-O1', 'FP1-F7', 'F7-T3', 'T3-T5', 'T5-O1', \
    'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2', 'FP2-F8', 'F8-T4', 'T4-T6', 'T6-O2', 'VEOG', 'HEOG', 'EKG']
    return z,labels
