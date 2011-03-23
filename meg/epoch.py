'''epoch data'''

from numpy import size, reshape, mean, shape, zeros, float32
from meg.fftmeg import nearest

def two2threeD(dataobj):
    try:
        dataobj.hdr
    except NameError:
        print 'your "data" does not appear to be the right object'
        return
    
    d = dataobj
    r = d.data_block.reshape(d.pnts_in_file / d.numofepochs, d.numofepochs, d.numofchannels,order='F') #2 to 3D
    return r
##
##def shapecontinious(dataobj, ind):
##    pass

def epochs(data, epochs, start, end):
    print 'epochs'
    numch = size(data,1)
    print shape(data), epochs, start, end, numch
    redata = data.reshape([size(data,0)/epochs, epochs, numch], order='F')
    print shape(redata)
    cutdata = redata[int(start):int(end),:]
    print shape(cutdata), int(start), int(end)
    data = cutdata.reshape(size(cutdata,0)*size(cutdata,1),size(cutdata,2),order='F')
    #adata = mean(cutdata,1)
    return data

def cont(data, start, end, ind):
    print 'continuious file epoching'
    
    n = zeros([int(start)+int(end),len(ind), size(data,1)], dtype=float32)
    print shape(n)
    #print int(start), int(end), len(ind)
    for eachtrial in range(0, len(ind)):
        
        try:
            #print shape(data[ind[eachtrial]-int(start):ind[eachtrial]+int(end)])
            print eachtrial
            n[:,eachtrial,:] = data[ind[eachtrial]-int(start):ind[eachtrial]+int(end)]
        except IndexError:
            pass
        except ValueError:
            print  eachtrial, len(ind)
            #if eachtrial == len(ind):
            print 'not enough data on last epoch to use. dropping last epoch'
            #n2 = zeros([size(n,0),size(n,1)-1,size(n,2)])
            n = n[:,:-1,:]; print shape(n)
            ind = ind[:-1]
    
    
    print shape(n)
    #return n

    #redata = data.reshape([size(data,0)/epochs, epochs, numch], order='F')
    #print shape(redata)
    #cutdata = redata[int(start):int(end),:]
    #print shape(cutdata)
    #adata = mean(cutdata,1)
    
    #--20090818--danc--changing returning value to be 3d epochs instead of 2D
    data = n.reshape(size(n,0)*size(n,1),size(n,2),order='F')
    
    return n

class cut():
    def __init__(self, dataobj, time, startsec, stopsec):
##def cut(dataobj, time, startsec, stopsec):
        r = two2threeD(dataobj)
        print 'were using seconds here not ms'
        indstart = nearest(time, startsec)
        indstop = nearest(time, stopsec)
        cutdata = r[indstart:indstop,:,:]
        self.data = cutdata.reshape(size(cutdata,0)*size(cutdata,1),size(cutdata,2),order='F')
        self.time = time[indstart:indstop]
        
        self.avg = mean(self.data.reshape(self.time.size, size(self.data,0)/self.time.size, size(self.data,1)),1)
        #return cutshaped
