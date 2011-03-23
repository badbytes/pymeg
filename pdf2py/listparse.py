'''listctrlparse'''

import os
from numpy import shape, mean, size
def megdata(parentitem, selitem, megdata):
    items = [('pnts_in_file', unicode(megdata.pnts_in_file[0])),\
    ('time_slice_size', unicode(megdata.time_slice_size)), \
    ('total_chans_in_file_on_disk', unicode(megdata.total_chans)), \
    ('total_chans', unicode(megdata.numofchannels)), \
    ('filename', unicode(megdata.filename)), \
    ('filepath', unicode(megdata.filepath)), \

    \
    ]
    return items

def header(parentitem, selitem, header):
    items = [('header_offset', unicode(header.header_offset[0]))]
    return items

def channel_ref_data(parentitem, selitem, hdr):
    items = [];
    for i in range(0, len(hdr.channel_ref_data)):
        items.append((str(i), unicode(eval('hdr.channel_ref_data[i].'+selitem))))
        
    print selitem
    #items = [(selitem, unicode(eval('hdr.channel_ref_data[0].'+selitem)))]
    return items

    for i in range(0, len(channel_ref_data)):
        channelrefitem = channel_ref_data[i].selitem[0]
        print channelrefitem
        #items.append(channel_ref_data[i].chan_label, unicode(channel_ref_data[i].selitem))
    return items

def header_data(parentitem, selitem, header_data):
    items = [('acq_mode', unicode(header_data.acq_mode[0])),\
    ('checksum', unicode(header_data.checksum[0])),\
    ('data_format', unicode(header_data.data_format[0])),\
    ('file_type', unicode(header_data.file_type[0])),\
    ('input_epochs', unicode(header_data.input_epochs[0])),\
    ('last_file_index', unicode(header_data.last_file_index[0])),\
    ('sample_period', unicode(header_data.sample_period[0])),\
    ('timestamp', unicode(header_data.timestamp[0])),\
    ('total_associated_files', unicode(header_data.total_associated_files[0])),\
    ('total_chans', unicode(header_data.total_chans[0])),\
    ('total_ed_classes', unicode(header_data.total_ed_classes[0])),\
    ('total_epochs', unicode(header_data.total_epochs[0])),\
    ('total_events', unicode(header_data.total_events[0])),\
    ('total_fixed_events', unicode(header_data.total_fixed_events[0])),\
    ('total_processes', unicode(header_data.total_processes[0])),\
    ('version', unicode(header_data.version[0])),\
    ('xaxis_label', unicode(header_data.xaxis_label[0])),\
    \
    ]
    return items



def epoch_data(parentitem, selitem, epoch_data):
    items = [('actual_iti', unicode(epoch_data.actual_iti[0])),\
    ('checksum', unicode(epoch_data.checksum[0])),\
    ('epoch_duration', unicode(epoch_data.epoch_duration[0])),\
    ('epoch_timestamp', unicode(epoch_data.epoch_timestamp[0])),\
    ('expected_iti', unicode(epoch_data.expected_iti[0])),\
    ('pts_in_epoch', unicode(epoch_data.pts_in_epoch[0])),\
    ('total_var_events', unicode(epoch_data.total_var_events[0])),\
    ]
    return items

def event_data(parentitem, selitem, event_data):
    items = [('checksum', unicode(event_data[0].checksum[0])),\
    ('end_lat', unicode(event_data[0].end_lat)),\
    ('fixed_event', unicode(event_data[0].step_size)),\
    ('name', unicode(event_data[0].name)),\
    ('start_lat', unicode(event_data[0].start_lat)),\
    ('step_size', unicode(event_data[0].step_size)),\
    ]
    return items
    
def headshape(parentitem, selitem, headshape):
    items = [('points', unicode(shape(headshape.hs_point))),\
    ('cz', unicode(headshape.index_cz)),\
    ('inion', unicode(headshape.index_inion)),\
    ('lpa', unicode(headshape.index_lpa)),\
    ('nasion', unicode(headshape.index_nasion)),\
    ('rpa', unicode(headshape.index_rpa)),\
    ]
    return items

def config(parentitem, selitem, cfg):
    items = [('channel_data', unicode(shape(cfg.channel_data))),\
    ('data_checksum', unicode(cfg.data_checksum)),\
    ('data_dap_hostname', unicode(cfg.data_dap_hostname)),\
    ('data_next_derived_channel_number', unicode(cfg.data_next_derived_channel_number)),\
    ('data_site_name', unicode(cfg.data_site_name)),\
    ('data_supply_freq', unicode(cfg.data_supply_freq)),\
    ('data_sys_options', unicode(cfg.data_sys_options)),\
    ('data_system_fixed_gain', unicode(cfg.data_system_fixed_gain)),\
    ('data_sys_type', unicode(cfg.data_sys_type)),\
    ('data_total_chans', unicode(cfg.data_total_chans)),\
    ('data_total_sensors', unicode(cfg.data_total_sensors)),\
    ('data_total_user_blocks', unicode(cfg.data_total_user_blocks)),\
    ('data_version', unicode(cfg.data_version)),\
    ('data_volts_per_bit', unicode(cfg.data_volts_per_bit)),\
    ('Xfm', unicode(cfg.Xfm)),\
    ]
    return items

def mr_header(parentitem, selitem, header):
    items = [];
    k = header.keys()
    for f in range(0, len(header)):
        items.append((k[f],unicode(header[k[f]])))
    return items

def leadfields(parentitem, selitem, lf):
    items = [];
    items = [('leadfields', unicode(shape(lf)))]
    return items
def grid(parentitem, selitem, grid):
    items = [];
    items = [('grid', unicode(shape(grid)))]
    return items

def timef(parentitem, selitem, tf):
    items = [];
    items = [('timef', unicode('timef'))]
    return items

def ica(parentitem, selitem, i):
    items = [];
    items = [('pre-processed data matrix', unicode(shape(i['X']))), \
    ('pre-whitened projection matrix', unicode(shape(i['K']))), \
    ('unmixing matrix', unicode(shape(i['W']))), \
    ('mixing matrix', unicode(shape(i['A']))), \
    ('source matrix', unicode(shape(i['S']))), \
    ]
    return items

def channels(parentitem, selitem, ch):
    items = [];
    #k = header.keys()
    for c in ch.channelsortedlabels:
        items.append((unicode(ch.channeltype) ,unicode(c)))
    return items

def trigger(parentitem, selitem, ch):
    items = [];
    for c in ch.channelsortedlabels:
        items.append((unicode(ch.channeltype) ,unicode(c)))
    return items

def fftpow(parentitem, selitem, fftfreqs, fftpow):
    #print shape(fftfreqs), shape(fftpow)
    items = [];
    m = mean(fftpow,1)
    for f in range(0,size(fftfreqs)):
        items.append((unicode(fftfreqs[f]) ,unicode(m[f])))
    return items
def fit(parentitem, selitem, fit):
    items = [];
    for c in range(0,size(fit.corr_mat)):
        items.append((unicode(fit.pos[c]) ,unicode(fit.corr_mat[c])))
    return items

def dipoles(parentitem, selitem, points):
    items = [];
    for c in range(0,size(points,0)):
        items.append((unicode(c) ,unicode(points[c])))
    return items
