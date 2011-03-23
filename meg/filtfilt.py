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

'''filtfilt.calc(data, srate ,Wn=[55.0,65.0],order=int, band="low|high|stop|notch"
filtfilt.calc(data, 1000 ,Wn=[55.0],order=2, band="low"'''


from numpy import vstack, hstack, eye, ones, zeros, linalg, \
newaxis, r_, flipud, convolve, matrix, array, shape, size
from scipy.signal import lfilter
from scipy.signal import butter

def lfilter_zi(b,a):
    #compute the zi state from the filter parameters. see [Gust96].

    #Based on:
    # [Gust96] Fredrik Gustafsson, Determining the initial states in forward-backward
    # filtering, IEEE Transactions on Signal Processing, pp. 988--992, April 1996,
    # Volume 44, Issue 4

    n=max(len(a),len(b))

    zin = (  eye(n-1) - hstack( (-a[1:n,newaxis],
                                 vstack((eye(n-2), zeros(n-2))))))

    zid=  b[1:n] - a[1:n]*b[0]

    zi_matrix=linalg.inv(zin)*(matrix(zid).transpose())
    zi_return=[]

    #convert the result into a regular array (not a matrix)
    for i in range(len(zi_matrix)):
      zi_return.append(float(zi_matrix[i][0]))

    return array(zi_return)



def filtfilt(b,a,data):
    #For now only accepting 1d arrays
    ntaps=max(len(a),len(b))
    edge=ntaps*3

    #2D arrays support
    if data.ndim == 1:
        data = array([data]).T #making 2d
    print 'N X Channel'
    fi = zeros(data.shape)
    for i in range(0, size(data,1)):
        x = data[:,i]

##    if x.ndim != 1:
##        raise ValueError, "Filiflit is only accepting 1 dimension arrays."

        #x must be bigger than edge
        if x.size < edge:
            raise ValueError, "Input vector needs to be bigger than 3 * max(len(a),len(b)."

        if len(a) < ntaps:
            a=r_[a,zeros(len(b)-len(a))]

        if len(b) < ntaps:
            b=r_[b,zeros(len(a)-len(b))]

        zi=lfilter_zi(b,a)

        #Grow the signal to have edges for stabilizing
        #the filter with inverted replicas of the signal
        s=r_[2*x[0]-x[edge:1:-1],x,2*x[-1]-x[-1:-edge:-1]]
        #in the case of one go we only need one of the extrems
        # both are needed for filtfilt

        (y,zf)=lfilter(b,a,s,-1,zi*s[0])

        (y,zf)=lfilter(b,a,flipud(y),-1,zi*y[-1])

        #return flipud(y[edge-1:-edge+1])
        fi[:,i] = flipud(y[edge-1:-edge+1])
    return fi

def calc(data, srate, Wn=[55.0,65.0], order=2, band='low'):
    '''filtfilt.calc(X, 1000 ,Wn=[55.0,65.0],order=2, band="low"'''
    if size(Wn) == 2:
        if band != 'stop':
            if band != 'notch':
                print 'Wn of 2 elements must go with "notch" filter or "stop"'
                return
    if band == 'low':
        if size(Wn) != 1:
            print 'Wn must be one element'
            return
    if band == 'high':
        if size(Wn) != 1:
            print 'Wn must be one element'
            return
    Wn = array(Wn, dtype='f')
    nyq = srate/2;
    [b,a]=butter(order,Wn/nyq,btype=band)
    y=filtfilt(b,a,data)
    return y


##function [Y NFFT f]=fftchans(EEG)
##
##% [Y NFFT f]=fftchans(EEG);
##% Ym=Y(somechannel,:);
##% figure;plot(f,2*abs(Ym(1:NFFT/2))) ;
##
##% n=nearest(f,25); %get nearest freq to 25hz
##% f25=Y(:,n);
##% f25r=real(f25);
##
##for i =1:size(EEG.data,1)
##    t=0:(EEG.pnts/EEG.srate)/EEG.pnts:(EEG.pnts/EEG.srate); % time in seconds
##    t=t(1:end-1);
##    %freq=10; %frequency
##    %somefreqhz = sin(2 * pi * freq' *t)/2; %make sine wave
##
##
##    Fs=EEG.srate;
##    T=1/Fs;
##    L=length(t);
##    NFFT = 2^nextpow2(L);
##    Yi = fft(EEG.data(i,:,:),NFFT)/L;
##    Ymean=mean(Yi,3);
##    Y(i,:)=Ymean;
##    f = Fs/2*linspace(0,1,NFFT/2);
##    %
##end
##%figure;plot(f,2*abs(Y(1:NFFT/2))) ;
##
##f25=Y(:,nearest(f,25));

if __name__=='__main__':

    from scipy.signal import butter
    from scipy import sin, arange, pi, randn

    from pylab import plot, legend, show, hold

    t=arange(0,1,.001)
    x=sin(2*pi*t*5)
    #xn=x + sin(2*pi*t*10)*.1
    n=sin(2*pi*t*40)
    #xn=x+randn(len(t))*0.25
    xn=x+(n*.5)

    lp = 2.0
    hp = 7.0
    sr = size(t)/2

    #[b,a]=butter(3,2.0*(10/200), btype='low')

    X = (array([lp,hp])/sr)

    #[b,a]=butter(3,X)#, btype='low')
    [b,a]=butter(2,X, btype='stop')
    print a
    print len(t)

    z=lfilter(b,a,xn)
    y=filtfilt(b,a,xn)

    plot(x,'c')
    hold(True)
    plot(xn,'k')
    #plot(z,'r')
    plot(y,'r')
    plot(n*.5,'b')


    legend(('original','noisy signal','filtfilt - butter 3 order'))
    hold(False)
    show()

