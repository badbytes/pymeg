"""Return sensors and headshape positions"""

from pdf2py import pdf, channel
from numpy import zeros, array, size, append, reshape

class headshape:
    def __init__(self, datapdf):
        p=pdf.read(datapdf)
        #self.hsa=array(pdfinstance.hs.hs_point)
        return 
        self.hsm=zeros((size(hsa),3))
        for i in range(len(hsa)):
            self.hsm[i,:]=( hsa[i].x, hsa[i].y, hsa[i].z);

class sensors:
    def __init__(self, datapdf):
        pdfinstance=pdf.read(datapdf)
        for i in range(0, size(pdfinstance.cfg.channel_data)):
            if i==1: #create empty array
                megchlpos=array([])
                megchupos=array([])
                refshpos=array([])
                megchldir=array([])
                megchudir=array([])
                refshdir=array([])
                
            if pdfinstance.cfg.channel_data[i].type==1: #get MEG positions in array
                megchlpos=append(megchlpos,pdfinstance.cfg.channel_data[i].device_data.loop_data[0].position)
                megchupos=append(megchupos,pdfinstance.cfg.channel_data[i].device_data.loop_data[1].position)
                megchldir=append(megchldir,pdfinstance.cfg.channel_data[i].device_data.loop_data[0].direction)
                megchudir=append(megchudir,pdfinstance.cfg.channel_data[i].device_data.loop_data[0].direction)
                
            if pdfinstance.cfg.channel_data[i].type==3: #get ref positions in array
                refshpos=append(refshpos,pdfinstance.cfg.channel_data[i].device_data.loop_data[0].position)
                refshdir=append(refshdir,pdfinstance.cfg.channel_data[i].device_data.loop_data[0].position)
                
        #reshape arrays
        megchlpos=megchlpos.reshape(size(megchlpos)/3,3)
        megchupos=megchupos.reshape(size(megchupos)/3,3)
        refshpos=refshpos.reshape(size(refshpos)/3,3)
        megchldir=megchldir.reshape(size(megchldir)/3,3)
        megchudir=megchudir.reshape(size(megchudir)/3,3)
        refshdir=refshdir.reshape(size(refshdir)/3,3)
        
        self.megchlpos=megchlpos
        self.megchupos=megchupos
        self.megchldir=megchldir
        self.megchudir=megchudir

    