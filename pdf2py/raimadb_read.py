''' record patient {
        /* personal info */
        unique  key char id[11];
        char    last_name[16];
        char    first_name[16];
        char    middle_name[16];
        long    birth_date; /*stored in yyyymmdd format */
        char    ethnic[13];
        char    home_phone[16];
        char    work_phone[16];
        char    address[41];
        char    apartment_number[5];
        char    city[26];
        char    state[21];
        char    country[16];
        char    zip_code[11];
        char    nationality[16];
        int handedness;
        int     gender;

db reader'''

try:from scipy.io.numpyio import *
except ImportError: from extra.numpyio import *
from numpy import char, reshape, array, append
from pdf2py import header_data, epoch_data, channel_ref_data, event_data
import os
 
def readpatient(db):
    fid=open(db, "r")
    fid.seek(0, os.SEEK_END)
    lastpos = fid.tell()
    print lastpos
    
    firstpatpos = 1036 
    id = []
    fid.seek(firstpatpos, os.SEEK_SET) #first patient offset 
    for i in range(0, (lastpos-firstpatpos)/11/2):
        id.append(fread(fid, 11, 'c','c',1))
        fid.seek(11, os.SEEK_CUR) #skip empty
    return id
##
##def findpid(db):
##    if db.split('/')[-1] == 'person':
##        

class readperson():
    def __init__(self, db):
        fid=open(db, "r")
        fid.seek(0, os.SEEK_END)
        lastpos = fid.tell()
        firstpatpos = 3992

        fid.seek(firstpatpos, os.SEEK_SET) #first patient offset 
        self.id=[];
        self.lname=[];
        self.fname=[];
        self.mname=[];
        self.dob=[];
        self.ethnic=[];
        self.hphone=[];
        self.wphone=[]
        self.address=[];
        self.aptnum=[];
        self.city=[];
        self.state=[];
        self.country=[];
        self.zipcode=[]
        self.nationality=[]
        self.handedness=[]
        self.gender=[]
        for i in range(0, (lastpos-firstpatpos)/874):
            print 'start',fid.tell()
            self.id.append(fread(fid, 11, 'c','c',0))
            self.lname.append(fread(fid, 16, 'c','c',0))
            self.fname.append(fread(fid, 16, 'c','c',0))
            self.mname.append(fread(fid, 16, 'c','c',0))
            fid.seek(1,os.SEEK_CUR)
            self.dob.append(fread(fid, 1, 'i','i',0))
            self.ethnic.append(fread(fid, 13, 'c','c',0))
            self.hphone.append(fread(fid, 16, 'c','c',0))
            self.wphone.append(fread(fid, 16, 'c','c',0))
            self.address.append(fread(fid, 41, 'c','c',0))
            self.aptnum.append(fread(fid, 5, 'c','c',0))
            self.city.append(fread(fid, 26, 'c','c',0))
            self.state.append(fread(fid, 21, 'c','c',0))
            self.country.append(fread(fid, 16, 'c','c',0))
            self.zipcode.append(fread(fid, 11, 'c','c',0))
            self.nationality.append(fread(fid, 16, 'c','c',0))
            fid.seek(3, os.SEEK_CUR) 
            print fid.tell()
            self.handedness.append(fread(fid, 1, 'i','i',0))
            self.gender.append(fread(fid, 1, 'i','i',0))
            fid.seek(36+26+6+6+(16*8)+(46*6), os.SEEK_CUR)
            fid.seek(1, os.SEEK_CUR) #patient lock
            fid.seek(139, os.SEEK_CUR) 
            print 'end',fid.tell()
            if fread(fid,1,'c','c',0) == '': #skip 450 bytes
                fid.seek(449, os.SEEK_CUR)
            else:
                fid.seek(-1, os.SEEK_CUR)
            
class readscan():
    def __init__(self, db):
        fid=open(db, "r")
        fid.seek(0, os.SEEK_END)
        lastpos = fid.tell()
        firstpatpos = 8704

        fid.seek(firstpatpos, os.SEEK_SET) #first patient offset 
        self.scan_name=[];
        self.scan_data_type=[];
        #for i in range(0, (lastpos-firstpatpos)/874):
        print 'start',fid.tell()
        fid.seek(46, os.SEEK_CUR) #skip some bytes
        self.id.append(fread(fid, 11, 'c','c',0))
        self.scan_name.append(fread(fid, 11, 'c','c',0))
            
            #cb1silfdFD
            
            
            
            
