# Copyright 2008 Dan Collins
#
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# And is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Build; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

# Credit goes to the Folks from EEGlab project, as some of their code was used.


'''timef module
from meg import timef
datapdf='/path2data/e,rfhp1.0Hz,COH
t = timef.initialize()
t.calc(datapdf, 'A1', freqrange=[5.0,250])
'''

from pdf2py import data,channel,pdf
from meg import offset, nearest
from numpy import *
import scipy.signal
import os
import time
from misc import progressbar

class get4Ddata:
    def __init__(self, datapdf, chlabel):
        ch=channel.index(datapdf, 'meg')
        chind=ch.channelindexhdr[ch.channelsortedlabels == chlabel]
        self.d=data.read(datapdf)
        self.d.getdata(0, self.d.pnts_in_file, chind)
        self.d.data_block=offset.correct(self.d.data_block)
        print self.d.data_block.shape
        self.p=pdf.read(datapdf)
        self.ext = 'pymtimef'


class initialize:
    '''tf = timef.initialize()'''

    def clean_overlaps(self):
        '''When asking for more timesout then exist in the truncated window
        you may end up with redundant time points. Let cut those out.'''
        time = self.timevals
        ind = []
        for i in range(0,len(time)):
            if i == 0:
                z = time[i]
            else:
                if time[i] == z:
                    ind.append(i)
                z = time[i]

        if len(ind) != 0:
            print 'cutting overlapping points'
            self.P = delete(self.P,ind,axis=1)
            self.Plog = delete(self.Plog,ind,axis=1)
            self.Ptrials = delete(self.Ptrials,ind,axis=1)
            self.timevals = delete(self.timevals,ind)
            self.timevect = delete(self.timevect,ind)
            self.timeindices = delete(self.timeindices,ind)

    def calc(self, data=None, chlabel=None, cycles=[3.0, 0.5], \
    freqrange=[5.0, 100],
    padratio=4, timesout=200, frames=None, trials=None, srate=None, eventtime=None):
        '''tf.calc(data=pm[:,25],frames = frames,srate=srate, trials=trials)
        tf.calc(fn[0], chlabel="A1", eventtime=300)
        frames = samples in an epoch
        eventtime is the offset to stimulus onset'''
        if data == None:
            print 'Need some data to work on..', 'data=datapdf, or data=signal'
            return
        else:
            if type(data) == ndarray:
                print 'not a datafile with a path'
                print 'I\'m guessing not a datafile, so your supplying the data and parameters (srate,trials,frames)'
                if frames == None:
                    print 'Fail. You need to provide number of frames (frames=(Epoch Duration/sample period)-1), (ex. (0.9997493/.00147456)-1)'
                    return
                if trials == None:
                    print 'Fail. You need to provide number of trials (trials=5)'
                    return
                if srate == None:
                    print 'Fail. You need to provide sample rate. (srate=678)'
                    return
                self.data=data
                srate = float(srate)
                self.srate=float(srate)
                sp=1/srate
            else:
                if os.path.isfile(data) == True:
                    print 'I think this is a 4D data file'
                    if chlabel == None:
                        print 'oops, you need to provide a chanlabel... chlabel="A1"'
                        return
                    else:
                        f=get4Ddata(data,chlabel)
                        self.data=f.d.data_block;
                        self.srate=float(1/f.p.hdr.header_data.sample_period)
                        print 'srate', self.srate
                        #frames=(f.p.hdr.epoch_data[0].epoch_duration/f.p.hdr.header_data.sample_period)-1
                        frames=int(f.p.hdr.epoch_data[0].epoch_duration/f.p.hdr.header_data.sample_period)#-1
                        self.frames=frames
                        #return
                        trials=size(f.p.hdr.epoch_data)
                        print 'trials', trials

                        sp=f.p.hdr.header_data.sample_period[0]

        ts=time.time()
        self.cutpnt=int(floor(shape(self.data)[0]/frames)*frames)
        self.data=self.data[0:self.cutpnt] #trim data #trim data to be int divisible by frames
        self.trials=trials
        self.freqrange=freqrange
        self.frames=frames

        self.winsize=2**(ceil(log2(abs(frames)))-3) #default winsize
        print 'winsize',self.winsize

        #reshape by frames
        print frames, shape(self.data)
        self.data=self.data.reshape([size(self.data,0)/frames, frames]).transpose(); #collapse across epochs
        self.nfreqs = self.winsize/2*padratio+1;
        #adjust nfreqs depending on frequency range
        tmpfreqs = linspace(0, self.srate/2, self.nfreqs);
        self.tmpfreqs = tmpfreqs[1:]; # remove DC (match the output of PSD)
        self.nfreqs = size(intersect1d(self.tmpfreqs[self.tmpfreqs >= self.freqrange[0]], self.tmpfreqs[self.tmpfreqs <= self.freqrange[1]]))
        freqs=linspace(self.freqrange[0], self.freqrange[1],self.nfreqs)
        self.freqs=freqs

        if len(cycles) == 2:
            if cycles[1] < 1:
                #print cycles, freqs
                cycles = ([cycles[0], cycles[0]*freqs[-1]/freqs[0]*(1-cycles[1])])
        self.cycles=cycles
        tlimits=array([0, frames/self.srate*1000])
        self.tlimits=tlimits

        def morlet(): #default wavelet
            print 'constructing wavelet'
            self.wavelet=[]
            timeresol=[]
            freqresol=[]
            for i in range(0, size(freqs)): #morlet wavelet
                timesupport=7;
                cycles = linspace(self.cycles[0], self.cycles[1], size(self.freqs))
                fk=freqs[i]
                sigf=fk/cycles[i]
                sigt=1/(2*pi*sigf)
                A=1/sqrt(sigt*sqrt(pi))
                timeresol.append(2*sigt)
                freqresol.append(2*sigf);
                #self.fk=fk;self.sigf=sigf;self.sigt=sigt;
                self.timeresol=timeresol
                self.freqresol=freqresol
                tneg=arange(-sp,-sigt*(timesupport/2),-sp)
                tpos=arange(0,sigt*(timesupport/2),sp)
                t=append(flipud(tneg),tpos)
                #self.tneg=tneg;self.tpos=tpos;self.t=t;self.sp=sp;self.sigf=sigf;self.sigt=sigt
                #self.A=A
                psi=A*(exp(-(t**2)/dot(2,(sigt**2)))*exp(2*1j*pi*fk*t));
                self.psi=psi
                self.wavelet.append(psi)
        morlet()


        #new winsize calc
        for index in range(0, len(self.wavelet)):
            self.winsize = max(self.winsize,len(self.wavelet[index]));

        #construct time vectors
        timevect = linspace(tlimits[0], tlimits[1], frames);
        self.srate = 1000*(frames-1)/(tlimits[1]-tlimits[0]);
        npoints=timesout
        wintime = 500*self.winsize/self.srate;
        timevals = linspace(tlimits[0]+wintime, tlimits[1]-wintime, npoints);
        self.timevect=timevect
        self.timevals=timevals
        self.wintime=wintime
        self.npoints=npoints

        #find closest points in data
        self.oldtimevals = timevals;
        timeindices=array([])
        for index in range(0, size(timevals)):
            ind = argmin(abs(timevect-timevals[index]))
            timeindices=append(timeindices, ind)
            timevals[index] = timevect[ind];
            self.timevals=timevals;self.timeindices=timeindices
            self.ind=ind
            self.timevect=timevect

        #other morlet
        def builtinmorlet(self):
            for i in range(0, size(freqs)): #morlet wavelet
                self.wavelet.append(scipy.signal.morlet)
            print 'wavelet size',len(self.wavelet)

        #repmat wavelet filter to match number of trials
        for index in range(0, size(freqs)):
            self.wavelet[index]=tile(self.wavelet[index],(trials,1)).transpose()
        print 'wavelet length',len(self.wavelet)
        self.tmpall=zeros([size(freqs),timesout,trials])*exp(1j)
        print 'calculating power and itc'
        pbar = progressbar.ProgressBar().start()
        for index in range(0, size(timeindices)):
            #print index,size(timeindices)#)*100
            pbar.update((float(index)/float(size(timeindices)))*100)
            for freqind in range(0, size(freqs)):
                wav = self.wavelet[freqind]; self.wav=wav
                sizewav = size(wav,0)-1
                self.sizewav=sizewav
                try:self.tmpX = self.data[array(linspace(-sizewav/2,sizewav/2,sizewav+1)+timeindices[index],dtype=int),:]
                except IndexError: print 'too few points in data to calculate that low of freq.\
                try increasing min freq, or load more points. exiting'; self.error_code = -2; return -2
                self.tmpX = self.tmpX - ones([size(self.tmpX,0),1])*mean(self.tmpX);
                self.tmpX = sum(wav * self.tmpX,0)
                self.tmpall[freqind, index, :] = self.tmpX;



        self.Ptrials=reshape(self.tmpall, [self.nfreqs, size(self.timevals)*trials], 'FORTRAN')
        self.P = float32(mean(self.tmpall*conj(self.tmpall),2)) # power
        self.PP = abs(self.tmpall)**2; #power
        #self.TP = sum(t.PP,2) / size(self.tmpall,2) #total power
#        case 'coher',       formula = [ 'sum(arg1,3)./sqrt(sum(arg1.*conj(arg1),3))/ sqrt(' int2str(trials) ');' ];
#        case 'phasecoher',  formula = [ 'mean(arg1,3);' ]; inputdata = alltfX./sqrt(alltfX.*conj(alltfX));
#        case 'phasecoher2', formula = [ 'sum(arg1,3)./sum(sqrt(arg1.*conj(arg1)),3);' ];

        self.pow_comp = mean(self.tmpall,2)
        self.Plog = 10*log10(self.P)
        #self.Plog = log10(self.P)
        #self.PlogRatio = log10(self.P/self.Pother)
        #ITC
        self.itcvals = sum(self.tmpall / sqrt(self.tmpall * conj(self.tmpall)) ,2) / size(self.tmpall,2);

        del self.tmpall, self.tmpX, self.oldtimevals, self.tmpfreqs
        if self.trials == 1:
            del self.pow_comp

        self.clean_overlaps()
        '''when timesout greater then resolution, \
        wavelets overlap and you get requndant times and values. \
        This function check for them and cuts them out sometimes leaving \
        timesout less than specified'''

        te=time.time()
        print 'elapsed time',te-ts
        del self.wavelet

        if eventtime != None:
            self.eventtimecorrect(eventtime)

    def eventtimecorrect(self, eventtime):
        '''shift time values from window time to eventtime.'''
        self.timevals = self.timevals - eventtime


    def tftplot(self, type='P', aspect='auto', eventoffset=None, freq=None):
        '''
        tftplot types
        type = 'P' for power
        type = 'Plog' for logpower
        type = 'itc' for phaselockingfactor
        type = 'itcreal' for realphaselockingfactor
        type = 'Ptrials' for nonaveraged power. power X trial
        type = 'Evoked Power' for evoked power
        eventoffset = 1000*p.data.eventtime[0]
        '''
        print 'type of plot', type
        from pylab import imshow, show, colorbar, xlabel, ylabel
        if type == 'P' or type == 'Power':
            data = abs(self.P)
            #if iscomplexobj(data):
        if type == 'Plog' or type == 'Log Power':
            data = abs(self.Plog)
        if type == 'Evoked Power':
            try:
                onsetind = nearest.nearest(self.timevals,0)[0]
                print onsetind
                data = abs(self.P) / array([mean(abs(self.P[:,:onsetind]),axis=1)]).T
            except:
                'cant do that dave'
        if type == 'Induced Power':
            try:
                onsetind = nearest.nearest(self.timevals,0)[0]
                print onsetind
                evoked = abs(self.P) / array([mean(abs(self.P[:,:onsetind]),axis=1)]).T
                data = abs(self.P) - evoked
            except:
                'cant do that dave'
        if type == 'itc' or type == 'Inter Trial Coherence':
            data = abs(self.itcvals)
        if type == 'itcreal' or type == 'Phase':
            data = real(self.itcvals)
        if type == 'Ptrials' or type == 'Trial Power': #power per trial
            data = abs(self.Ptrials)
        if type == 'trialphase' or type == 'Trial Phase':
            ind = nearest.nearest(self.freqs, freq)
            data = squeeze(real(self.Ptrials[ind])).reshape((self.trials,self.npoints),order='C')
            xlab = 'time'
            ylab = 'trials'
        if eventoffset != None:
            self.timevals = self.timevals+eventoffset


        imshow(data,aspect=aspect, extent=(int(self.timevals[0]), int(self.timevals[-1]), \
        int(self.freqrange[1]), int(self.freqrange[0])));
        try:
            xlabel(xlab)
            ylabel(ylab)
        except:
            pass
        show()
        #colorbar()

        return data




