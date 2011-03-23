

'''save pymeg data'''

import pickle

def writedata(dataobj, filename2save):
    'write out dataobj into binary file'
    try:
        dataobj.ext
    except AttributeError:
        print 'unknown extension type, saving as .pym'
        ext = 'pym'
    else:
        ext = dataobj.ext
        
    print 'saving', filename2save+'.'+ext
    #fileout = filename2save+'.'+ext
    fo = open(filename2save+'.'+ext, 'wb')
    pickle.dump(dataobj, fo, pickle.HIGHEST_PROTOCOL)
    fo.close()
    
def readdata(filename2open):
    'read binary file'
    fo = open(filename2open, 'rb')
    data = pickle.load(fo)
    fo.close()
    return data

