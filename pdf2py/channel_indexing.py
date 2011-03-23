from pdf2py import config, header
import os

class indexing:
    def __init__(self, datapdf):
        if os.path.isfile(datapdf)==True:
            print 'reading pdf header', os.path.abspath(datapdf)
            self.hdr=header.read(datapdf);
            if os.path.isfile(os.path.dirname(datapdf)+'/config')==True:
                print 'found config file in same dir. Reading config'
                self.cfg=config.read(os.path.dirname(datapdf)+'/config');
            if os.path.isfile(os.path.dirname(datapdf)+'/hs_file')==True:
                print 'found headshape file in same dir. Reading headshape'  
                self.hs=headshape.read(os.path.dirname(datapdf)+'/hs_file');          
            
        
##conf=config.read('file')
##h=header.read('file')
##
##
## os.path.dirname(pdf)
##
##
##j=[];
##
##for i in range(0, len(h.channel_ref_data)):
##    j.append(h.channel_ref_data[i].chan_label)
##    
##    
##dd={}
## for x in range(0, len(j)):
##    dd[j[x]]=int(ind[x])