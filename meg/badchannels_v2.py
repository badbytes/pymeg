# Copyright 2008-2009 Dan Collins
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


'''badchannel detector
step1: calc distance between all channels
step2: calc the channel varience either across time or across channel
with optional freq notching
step3: for each channel, create a family. a family is neighboring channels within 1.5*the closest channel
step4: compare the varience between each channel and the median of its family.
and finally: determine baddness based on the ratio of each channel to its family.
'''

def fft_method(data, srate, epochs, neighbors):
    from meg import fftmeg
    '''fftmeg.calc(p.data.data_block, p.data.srate,epochs=p.data.numofepochs)'''
    fftout = fftmeg.calc(data, srate,epochs=epochs)
    for i in arange(size(data,1)): #for each channel get

def calc(datapdf, fftdata, chinstance, thresh=2, datatoremove='none',chvar='no', chfreq='yes', freqarray='freqvals', minhz=3, maxhz=200, powernotch='yes'):
    '''bad = badchannels.calc(datapdf, pow, ch,thresh=2, chfreq='yes', freqarray=freq, maxhz=200,powernotch='yes')'''

    data2thresh = copy(fftdata)
    s = sensors.locationsbyindex(datapdf, chinstance.channelindexcfg)
    p = pdf.read(datapdf)
    distmat=zeros([size(s.chlpos ,0), size(s.chlpos ,0)]); #create empty matrix 248X248

    for i in range(0,size(s.chlpos,0)):# %get euclid dist between all pairs of channels
        for ii in range(0,size(s.chlpos ,0)):
            distmat[i,ii] = euclid(s.chlpos[i,0], s.chlpos[ii,0],\
            s.chlpos[i,1], s.chlpos[ii,1], \
            s.chlpos[i,2], s.chlpos[ii,2]);

    if chvar == 'yes':
        ChanDetMat = array([var(data2thresh,axis=0)])
        print 'calculating channel variance across time'
        varmat = zeros([1, size(data2thresh ,1)]);


    elif chfreq == 'yes':
        print 'using fft provided'
        if len(shape(data2thresh)) == 1:
            data2thresh = array([data2thresh])
        varmat = zeros([size(data2thresh ,0),size(data2thresh ,1) ]);
        ChanDetMat = data2thresh

        n=array([])
        try:
            if type(freqarray) == str:
                print 'need to load freq indices. error1'
                return
            freq = freqarray
            lowfreq = nearest(freq, [0,minhz])
            data2thresh[lowfreq[0]:lowfreq[1],:] = 0 #zero poweline
            if powernotch == 'yes':
                powerline = nearest(freq, [56,64])
                data2thresh[powerline[0]:powerline[1],:] = 0 #zero poweline
                powerline = nearest(freq, [116,124])
                data2thresh[powerline[0]:powerline[1],:] = 0 #zero poweline
                powerline = nearest(freq, [176,186])
                data2thresh[powerline[0]:powerline[1],:] = 0 #zero poweline

            #nyq = nearest(freq, [(1/p.hdr.header_data.sample_period)[0]/2])
            maxhz = nearest(freq, maxhz)
            data2thresh[maxhz[0]:,:] = 0 #zero above some value. must be at the lowpass. ex. 200hz
            #return data2thresh
        except AttributeError:
            print 'need to load freq indices'


    matall = zeros([size(data2thresh ,0),size(data2thresh ,1) ]);

    for v in range(0, size(data2thresh, 0)):

        for j in range(0,size(distmat,1)):
            closestchdist = min(distmat[j,logical_and(distmat[j,:] < .05, distmat[j,:] > .0)])
            jfamily = logical_and(distmat[j,:] < closestchdist*1.5, distmat[j,:] > .0);
            jmedianvar=median(ChanDetMat[v,jfamily]);
            jvar=ChanDetMat[v,j];
            jratio=jvar/jmedianvar;
            matall[v,j] = jratio


    minmat = nanmin(matall, axis=0)
    maxmat = nanmax(matall, axis=0)
    badch = chinstance.channelsortedlabels[maxmat>thresh]
    badch = append(badch,chinstance.channelsortedlabels[minmat<1/thresh])

    badmaxind = maxmat>thresh
    badminind = minmat<1/thresh
    badind = badmaxind+badminind
    goodind = badind == False

    print 'bad channels',badch

    if datatoremove != 'none':
        data2thresh = datatoremove[:,logical_and(maxmat<thresh,minmat>(1.0/thresh))]
    else:
        data2thresh = data2thresh[:,logical_and(maxmat<thresh,minmat>(1.0/thresh))]

    #090615 modify output to be dict instead of truples.
    baddict = {}
    baddict['datamat'] = badch
    baddict['badch'] = badch
    baddict['ratios'] = matall
    baddict['maxratios'] = nanmax(matall, axis=0)
    baddict['badind'] = badind
    baddict['goodind'] = goodind

    return baddict #data2thresh, badch, matall, nanmax(matall, axis=0)

if __name__=='__main__':
    calc()
