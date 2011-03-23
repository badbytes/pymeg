"""Return sensors and headshape positions"""

from pdf2py import pdf
from numpy import zeros, array, size, append, reshape
from pylab import *
##try:
##    import matplotlib.axes3d as p3
##import pylab as p

class locations:
    def __init__(self, datapdf, channelinstance):
        pdfinstance=pdf.read(datapdf)
        chlpos=array([]);chupos=array([])
        chldir=array([]);chudir=array([])
        for i in channelinstance.channelindexcfg: 
            chlpos=append(chlpos,pdfinstance.cfg.channel_data[i].device_data.loop_data[0].position)
            chupos=append(chupos,pdfinstance.cfg.channel_data[i].device_data.loop_data[1].position)
            chldir=append(chldir,pdfinstance.cfg.channel_data[i].device_data.loop_data[0].direction)
            chudir=append(chudir,pdfinstance.cfg.channel_data[i].device_data.loop_data[1].direction)
                
        #reshape arrays
        chlpos=chlpos.reshape(size(chlpos)/3,3)
        chupos=chupos.reshape(size(chupos)/3,3)
        chldir=chldir.reshape(size(chldir)/3,3)
        chudir=chudir.reshape(size(chudir)/3,3)
        
        self.chlpos=chlpos
        self.chupos=chupos
        self.chldir=chldir
        self.chudir=chudir
   
        
