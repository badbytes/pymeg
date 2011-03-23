import os
from numpy import size,unique
from pdf2py import header

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
                #print 'scans',scan
                if size(scan) > 0:
                    for iii in scan:
                        xx = os.walk(stage+'/data/'+i+'/'+ii+'/'+iii) #added 090324 to fix bug
                        session = xx.next()[1]
                        #print 'scan',iii,'sessions',session
                        for iiii in session: #added 090324 to fix bug
                            #print iiii
                        #if size(session) > 0: #removed 090324 to fix bug
                            xx = os.walk(stage+'/data/'+i+'/'+ii+'/'+iii+'/'+iiii) #added 090324 to fix bug
                            run = xx.next()[1]
                            #print 'run',run
                            if size(run) > 0:
                                data = xx.next()
                                #print 'data',data
                                if size(data[2]) > 0:
                                    for d in data[2]:
                                        #try and read
                                        #print data[0]+'/'+d
                                        try:
                                            h = header.read(data[0]+'/'+d)
                                            if h.header_offset[0] > 0:
                                                dirofscans[iii] = data[0]+'/'+d
                                                #print 'dirofscans',dirofscans
                                        except IOError:
                                            pass
                                        except MemoryError:
                                            pass
                                        except OverflowError:
                                            pass
                                        except AttributeError:
                                            print 'Attribute Error in dbscan'
                                        except IndexError:
                                            pass
                                        



                                    #dirofscans[iii] = data[0]+data[2][0]
                                    #listofscans.extend(iii)
                    #listofids.extend(dirs)

    uscans = unique(listofscans)
    return dirofscans

def tree(rootdir):
    x = os.walk(rootdir)
    scan = x.next()



if __name__ == '__main__':
    tree('/opt/msw/data/sam_data0/')
    run()
