'''epoch data'''

from meg.fftmeg import nearest

def reshapemeg(dataobj):
    try:
        dataobj.hdr
    except NameError:
        print 'your "data" does not appear to be the right object'
        return
    
    d = dataobj
    d.data_block = d.data_block.reshape(d.pnts_in_file / d.numofepochs, d.numofepochs, d.numofchannels) #2 to 3D

def cut(reshapemeg, time, startsec, stopsec):
    print 'were using seconds here not ms'
    indstart = nearest(time, startsec)
    indstop = nearest(time, endsec)
    cutdata = d.data_block[indstart:indstop,:]
    return cutdata
