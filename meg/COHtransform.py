#!/usr/bin/env python

import subprocess
from numpy import *
from pdf2py import headshape, config
from mri import transform
from meg import plotvtk

def calc(configpath, hspath):
    s = subprocess.Popen('print_coh -posted', shell=True, stdout=subprocess.PIPE)
    out = s.stdout.readlines()
    
    #z = !print_coh -posted
    lpa=out[9].split()
    rpa=out[10].split()
    nas=out[11].split()
    cz=out[12].split()
    ini=out[13].split()
    
##    while True:
##        try: 
##            cz.remove('');#lpa.remove('');rpa.remove('');nas.remove('');ini.remove('');
##        except ValueError:
##            break
        
    cz.pop();lpa.pop();rpa.pop();nas.pop();ini.pop();
    coh_cz = [];coh_lpa = [];coh_rpa = [];coh_nas = []; coh_ini = [];
    
    for i in range(0, size(cz)):
        coh_lpa.append(eval(lpa[i]))
        coh_rpa.append(eval(rpa[i]))
        coh_nas.append(eval(nas[i]))
        coh_cz.append(eval(cz[i]))
        coh_ini.append(eval(ini[i]))
    
    h = headshape.read(hspath)


    nasdiff = h.index_nasion - h.index_cz
    sensorframe_nasion = coh_cz + nasdiff*100
    [t,r]=transform.meg2meg(coh_lpa, coh_rpa, sensorframe_nasion)

    #datafile = '/opt/msw/data/spartan_data0/1337/sef+eeg/03%31%09@11:17/1/config'
    c = config.read(configpath)
    chl = array([]); chu = array([]); gradchl = array([])

    for i in range(0, c.data_total_chans):
        if c.channel_data[i].type == 1:# or c.channel_data[i].type == 3: #transform it
            chl = append(chl, c.channel_data[i].device_data.loop_data[0].position)#*100)
            chu = append(chu, c.channel_data[i].device_data.loop_data[1].position)#*100)
        elif c.channel_data[i].type == 3:
            gradchl = append(chl, c.channel_data[i].device_data.loop_data[0].position)#*100)
            
    chlpos = chl.reshape(3,size(chl)/3, order='F')
    chupos = chu.reshape(3,size(chu)/3, order='F')
    gradchlpow = gradchl.reshape(3,size(gradchl)/3, order='F')

    signalup_headframe = transform.mri2meg(t,r,chupos)
    signallow_headframe = transform.mri2meg(t,r,chlpos)
    grad_headframe = transform.mri2meg(t,r,gradchlpow)
    #return signallow_headframe
    signalcount = 0
    gradcount = 0
    for i in range(0, c.data_total_chans):
        if c.channel_data[i].type == 1:# or c.channel_data[i].type == 3: #transform it
            c.channel_data[i].device_data.loop_data[0].position = signalup_headframe[:,signalcount]
            c.channel_data[i].device_data.loop_data[1].position = signallow_headframe[:,signalcount]
            signalcount = signalcount + 1
        if c.channel_data[i].type == 3:
            c.channel_data[i].device_data.loop_data[0].position = grad_headframe[:,gradcount]
            gradcount = gradcount + 1
    
    config.write(configpath, c)
    return c

    plotvtk.display(h.hs_point, signallow_headframe.T/100)
    
    