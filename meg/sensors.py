"""Return sensors and headshape positions"""
'''sensors.locationsbyindex(datapdf, ch.channelindexcfg)'''
from pdf2py import pdf, channel
from numpy import zeros, array, size, append, reshape

class locations:
    def __init__(self, datapdf):
        '''returns unsorted meg signal sensors... A1,A2,etc'''
        pdfinstance=pdf.read(datapdf)
        for i in range(0, size(pdfinstance.cfg.channel_data)):
            if i==1: #create empty array
                megchlpos=array([])
                megchupos=array([])
                refshpos=array([])
                megchldir=array([])
                megchudir=array([])
                refshdir=array([])
                self.name = array([])

            if pdfinstance.cfg.channel_data[i].type==1: #get MEG positions in array
                #megchlpos2=append(megchlpos,pdfinstance.cfg.channel_data[pdfinstance.cfg.channel_data[223].chan_no-1].device_data.loop_data[0].position)
                megchlpos=append(megchlpos,pdfinstance.cfg.channel_data[i].device_data.loop_data[0].position)
                megchupos=append(megchupos,pdfinstance.cfg.channel_data[i].device_data.loop_data[1].position)
                megchldir=append(megchldir,pdfinstance.cfg.channel_data[i].device_data.loop_data[0].direction)
                megchudir=append(megchudir,pdfinstance.cfg.channel_data[i].device_data.loop_data[1].direction)
                self.name = append(self.name, pdfinstance.cfg.channel_data[i].name)
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
        
class locationsbyindex:
    def __init__(self, datapdf, index):
        '''returns sensor locations from an index provided
        sensors.locationsbyindex(datapdf, ch.channelindexcfg)'''
        pdfinstance=pdf.read(datapdf)
        self.chlpos=array([]);self.chupos=array([])
        self.chldir=array([]);self.chudir=array([])
        self.chname = array([])
        for i in index:
            self.chupos = append(self.chupos,pdfinstance.cfg.channel_data[i].device_data.loop_data[0].position)
            self.chlpos = append(self.chlpos,pdfinstance.cfg.channel_data[i].device_data.loop_data[1].position)
            self.chudir = append(self.chudir,pdfinstance.cfg.channel_data[i].device_data.loop_data[0].direction)
            self.chldir = append(self.chldir,pdfinstance.cfg.channel_data[i].device_data.loop_data[1].direction)
            self.chname = append(self.chname, pdfinstance.cfg.channel_data[i].name)
            
        
        self.chupos=self.chupos.reshape(size(self.chupos)/3,3)
        self.chlpos=self.chlpos.reshape(size(self.chlpos)/3,3)
        self.chudir=self.chudir.reshape(size(self.chudir)/3,3)
        self.chldir=self.chldir.reshape(size(self.chldir)/3,3)

