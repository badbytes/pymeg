'''trigger detect, return indices of zero value to nonzero change in trigger channel'''
from numpy import array, nonzero

class get:
    def __init__(self, unsorteddatachunk, channelinstance, trigtype):
        #trigtype=='TRIGGER' OR 'RESPONSE'
        #trig=trigdet.get(d.data_blockunsorted, ch, 'RESPONSE')
        '''channelstruct=channel.index(f, 'trig')'''

        trigchpos=channelinstance.sortedind[channelinstance.sortedch==trigtype]
        #trigchpos=channelstruct.sortedindtype[channelstruct.sortedindtype[channelstruct.sortedlabeltype=='TRIGGER']]
        self.trigdata = unsorteddatachunk[:,trigchpos[0]]
        trigpositive=array(nonzero(unsorteddatachunk[:,trigchpos[0]]))
        nonzeropulsebool=unsorteddatachunk[trigpositive,trigchpos[0]]+unsorteddatachunk[trigpositive-1,trigchpos[0]]==unsorteddatachunk[trigpositive,trigchpos[0]]
        self.trigstartind=array(trigpositive[nonzeropulsebool][1::])

        #for debugging
        self.nz = nonzeropulsebool
        self.tp = trigpositive
        self.trigchpos = trigchpos
