# Continuous wavelet transfrom via Fourier transform
# Collection of routines for wavelet transform via FFT algorithm


#-- Some naming and other conventions --
# use f instead of omega wherever rational/possible
# *_ft means Fourier transform

#-- Some references --
# [1] Mallat, S.  A wavelet tour of signal processing
# [2] Addison, Paul S. The illustrated wavelet transform handbook

import numpy
from numpy.fft import fft, ifft, fftfreq

#try:
#    from scipy.special import gamma
#except:



pi = numpy.pi

class DOG:
    """Derivative of Gaussian, general form"""
    # Incomplete, as the general form of the mother wavelet
    # would require symbolic differentiation.
    # Should be enough for the CWT computation, though

    def __init__(self, m = 1.):
        self.order = m
        self.fc = (m+.5)**.5 / (2*pi)
    
    def psi_ft(self, f):
        c = 1j**self.order / numpy.sqrt(gamma(self.order + .5)) #normalization
        w = 2*pi*f
        return c * w**self.order * numpy.exp(-.5*w**2)

class Mexican_hat:
    def __init__(self, sigma = 1.0):
        self.sigma = sigma
        self.fc = .5 * 2.5**.5 / pi
    def psi_ft(self, f):
        """Fourier transform of the Mexican hat wavelet"""
        c = numpy.sqrt(8./3.) * pi**.25 * self.sigma**2.5 
        wsq = (2. * pi * f)**2.
        return -c * wsq * numpy.exp(-.5 * wsq * self.sigma**2.)
    def psi(self, tau):
        """Mexian hat wavelet as described in [1]"""
        xsq = (tau / self.sigma)**2.
        c = 2 * pi**-.25 / numpy.sqrt(3 * self.sigma) # normalization constant from [1]
        return c * (1 - xsq) * numpy.exp(-.5 * xsq)
    def set_f0(self, f0):
        pass

class Morlet:
    def __init__(self, f0 = 1.5):
        self.set_f0(f0)
    def psi_ft(self, f):
        """Fourier transform of the approximate Morlet wavelet
            f0 should be more than 0.8 for this function to be correct."""
        return (pi**-.25) * (2.**.5) * numpy.exp(-.5 * (2. * pi * (f - self.fc))**2.)
    def set_f0(self, f0):
        self.f0 = f0
        self.fc = f0


def cwt_a(signal, scales, sampling_scale = 1.0, wavelet=Mexican_hat()):
    """ Continuous wavelet transform via fft. Scales version.  """
    signal_ft = fft(signal)                     # FFT of the signal
    W = numpy.zeros((len(scales), len(signal)),'complex') # create the matrix beforehand
    ftfreqs = fftfreq(len(signal), sampling_scale)       # FFT frequencies

    # Now fill in the matrix
    for n,s in enumerate(scales):
        psi_ft_bar = numpy.conjugate(wavelet.psi_ft(s * ftfreqs))
        W[n,:] = (s**.5) * ifft(signal_ft * psi_ft_bar)
    return W


def cwt_f(signal, freqs, Fs=1.0, wavelet = Morlet()):
    """Continuous wavelet transform -- frequencies version"""
    scales = wavelet.fc/freqs
    dt = 1./Fs
    return cwt_a(signal, scales, dt, wavelet)

