import os
from numpy import size,unique

def run():
    stage = os.environ['STAGE']
    #path = stage+'/data/'
    x=os.walk(stage+'/data/')
    datapaths = x.next()[1]
    listofscans = []
    dirofscans = {}

    for i in datapaths:
        x=os.walk(stage+'/data/'+i)
        dirs = x.next()[1]
        if size(dirs) > 0:
            for ii in dirs:
                xx = os.walk(stage+'/data/'+i+'/'+ii)
                scan = xx.next()[1]
                if size(scan) > 0:
                    for iii in scan:
                        session = xx.next()[1]
                        if size(session) > 0:
                            run = xx.next()[1]
                            if size(run) > 0:
                                data = xx.next()
                                
                                if size(data[2]) > 0:
                                    
                                    
                                    dirofscans[iii] = data[0]
                                    listofscans.extend(iii)
                    #listofids.extend(dirs)
    
    uscans = unique(listofscans)
    return dirofscans
                
if __name__ == '__main__':
    run()                
