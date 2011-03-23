
try:from scipy.io.numpyio import *
except ImportError: from extra.numpyio import *
import os
from time import strftime
import shutil

class getpoints:
    def __init__(self, elfile):
        datetime = strftime("%Y-%m-%d %H:%M:%S").replace(' ', '_')
        self.elfile = elfile
        if os.path.isfile(elfile) == True:
            print 'step 1: is file.'
            #if os.path.isfile(elfile) == True:
            #    print 'detecting previous attempted fix'
            shutil.copy(elfile, elfile+datetime)
        
        fileopen = open(elfile, 'r')
        
        fileopen.seek(0, os.SEEK_SET) #24bytes
        self.lpa = fread(fileopen, 3, 'd', 'd', 0)
        fileopen.seek(64, os.SEEK_SET) #24bytes
        self.rpa = fread(fileopen, 3, 'd', 'd', 0)
        fileopen.seek(128, os.SEEK_SET) #24bytes
        self.nas = fread(fileopen, 3, 'd', 'd', 0)
        fileopen.seek(192, os.SEEK_SET) #24bytes
        self.cz = fread(fileopen, 3, 'd', 'd', 0)
        fileopen.seek(256, os.SEEK_SET) #24bytes
        self.ini = fread(fileopen, 3, 'd', 'd', 0)

        fileopen.seek(320, os.SEEK_SET) #24bytes
        self.coil1 = fread(fileopen, 3, 'd', 'd', 0)
        fileopen.seek(384, os.SEEK_SET) #24bytes
        self.coil2 = fread(fileopen, 3, 'd', 'd', 0)
        fileopen.seek(448, os.SEEK_SET) #24bytes
        self.coil3 = fread(fileopen, 3, 'd', 'd', 0)
        fileopen.seek(512, os.SEEK_SET) #24bytes
        self.coil4 = fread(fileopen, 3, 'd', 'd', 0)
        fileopen.seek(576, os.SEEK_SET)
        self.coil5 = fread(fileopen, 3, 'd', 'd', 0)
        
class read(getpoints):
    def write(self):
        filewrite = open(self.elfile, 'r+')
        filewrite.seek(0, os.SEEK_SET) #24bytes
        fwrite(filewrite, 3, self.lpa, 'd', 1)
        filewrite.seek(64, os.SEEK_SET) #24bytes
        fwrite(filewrite, 3, self.rpa, 'd', 1)
        filewrite.seek(128, os.SEEK_SET) #24bytes
        fwrite(filewrite, 3, self.nas, 'd', 1)
        filewrite.seek(192, os.SEEK_SET) #24bytes
        fwrite(filewrite, 3, self.cz, 'd', 1)
        filewrite.seek(256, os.SEEK_SET) #24bytes
        fwrite(filewrite, 3, self.ini, 'd', 1)

        filewrite.seek(320, os.SEEK_SET) #24bytes
        fwrite(filewrite, 3, self.coil1, 'd', 1)
        filewrite.seek(384, os.SEEK_SET) #24bytes
        fwrite(filewrite, 3, self.coil2, 'd', 1)
        filewrite.seek(448, os.SEEK_SET) #24bytes
        fwrite(filewrite, 3, self.coil3, 'd', 1)
        filewrite.seek(512, os.SEEK_SET) #24bytes
        fwrite(filewrite, 3, self.coil4, 'd', 1)
        filewrite.seek(576, os.SEEK_SET)
        fwrite(filewrite, 3, self.coil5, 'd', 1)
        print 'step two: finished fixing byte swap'
    
    
