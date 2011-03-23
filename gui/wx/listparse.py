'''listctrlparse'''

import os

def hdrdata(parentitem, selitem, header_data):
    retlist = [('acq_mode', header_data.acq_mode[0]),\
    ('acq_mode', header_data.acq_mode[0]),\
    ('checksum', header_data.checksum[0]),\
    ('data_format', header_data.data_format[0]),\
    ('file_type', header_data.file_type[0]),\
    ('input_epochs', header_data.input_epochs[0]),\
    ('last_file_index', header_data.last_file_index[0]),\
    ('reserved', header_data.reserved[0]),\
    ('sample_period', header_data.sample_period[0]),\
    ('timestamp', header_data.timestamp[0]),\
    ('total_associated_files', header_data.total_associated_files[0]),\
    ('total_chans', header_data.total_chans[0]),\
    ('total_ed_classes', header_data.total_ed_classes[0]),\
    ('total_epochs', header_data.total_epochs[0]),\
    ('total_events', header_data.total_events[0]),\
    ('total_fixed_events', header_data.total_fixed_events[0]),\
    ('total_processes', header_data.total_processes[0]),\
    ('version', header_data.version[0]),\
    ('xaxis_label', header_data.xaxis_label[0]),\
    \
    ]

def epochdata(epoch_data):
    pass
