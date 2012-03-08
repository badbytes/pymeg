#       SSS.py
#
#       Copyright 2010 dan collins <danc@badbytes.net>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#####B=-VV
from numpy import *
import math


def script():

    fn = ['/home/danc/vault/decrypted/programming/python/data/meg/0611SEF/e,rfhp1.0Hz,n,x,baha001-1SEF,f50lp']
    #from gui.gtk import filechooser
    #fn = filechooser.open()
    from pdf2py import pdf
    p = pdf.read(fn[0])
    p.data.setchannels('meg')
    p.data.getdata(0,p.data.pnts_in_file)
    p.data.channels.getposition()
    #chA1pos = p.data.channels.chlpos[0]
    centofsphere = array([0,0,0]) #center of sphere
    chlpos_ = p.data.channels.chlpos - centofsphere
    chupos_ = p.data.channels.chupos - centofsphere
    from meg import euclid
    #Din = euclid.dist(centofsphere, p.data.channels.chlpos)
    Din = euclid.dist(array([0,0,0]), chlpos_)
    chmin = Din.argmin(); r_min = Din.min()
    #Dout = euclid.dist(centofsphere, p.data.channels.chupos)
    Dout = euclid.dist(array([0,0,0]), chupos_)
    chmax = Dout.argmax(); r_max = Dout.max()

    #_____________________
    #simsource
    from meg import leadfield_parallel as leadfield
    from meg import simsource
    xyz=array([ 12.5, -56.6 ,  82.0]) #in mm
    qxqyqz=array([.8,.078,1.578])
    from meg import makesine
    ms = makesine.create(1000, 1/p.hdr.header_data.sample_period, 5)
    lfin = leadfield.calc(p.data.channels, xyz)
    s = simsource.calc(lfin, xyz, qxqyqz)
    #s=s[0,:,:]
    simd = dot(ms,array([s]))


    #x = chA1pos[0]; y = chA1pos[1]; z=chA1pos[2]
    #r = sqrt((x**2)+(y**2)+(z**2))
    x = chlpos_[chmin][0]; y = chlpos_[chmin][1]; z=chlpos_[chmin][2]
    phi = math.atan2(z, sqrt(x**2 + y**2)); #phi = arccos(z/r)
    theta = math.atan2(y,x)

    def cart2sph(chpos):
        x = chpos[0]; y = chpos[1]; z=chpos[2]
        r = sqrt((x**2)+(y**2)+(z**2))
        phi = math.atan2(z, sqrt(x**2 + y**2)); #phi = arccos(z/r)
        theta = math.atan2(y,x)
        return r,phi,theta

    r_in=[];phi_in=[];theta_in=[];
    r_out=[];phi_out=[];theta_out=[];
    for i in range(0, size(chlpos_,0)): #for each channel
        Rin,Pin,Tin = cart2sph(chlpos_[i])
        Rout,Pout,Tout = cart2sph(chupos_[i])
        r_in.append(Rin);phi_in.append(Pin);theta_in.append(Tin)
        r_out.append(Rout);phi_out.append(Pout);theta_out.append(Tout)

    #r,phi,theta =cart2sph(p.data.channels.chlpos[chmin]-cos) #sperical coords in relation to center of sphere


    from scipy import special
    #s = special.sph_harm(-1,7,theta,phi)

    Sin = []; r_in = array(r_in)
    labels = []
    for L in range(1, 9):
        for M in range(-L, L+1):
            print('M:',M,'N:',L)
            labels.append(str(L)+','+str(M))
            Sin = append(Sin, special.sph_harm(M,L,theta_in,phi_in)/r_in**(L+1))

    Sin = Sin.reshape(len(Sin)/len(theta_in), len(theta_in))
    return Sin,simd

    #s = dot(sim_mix, Sin.T)
    #d = dot(s,Sin)

    #Sout = []; r_out = array(r_out)
    #for L in range(1, 7):
        #for M in range(-L, L):
            #Sout = append(Sout, special.sph_harm(M,L,theta_out,phi_out)*(r_out**(L-1)))

    #Sout = Sout.reshape(len(Sout)/len(theta_out), len(theta_out))



    #sss=zeros(shape(p.data.data_block))
    #for i in range(0, size(p.data.channels.chlpos,0)):
        #sss[:,i] = dot(array([p.data.data_block[:,i]]).T, dot(real(tmp),imag(tmp)))[:,0]




    #from pylab import *
    #from scipy import special
    #a_th = []
    ## list to store polar angle theta from -90 to + 90 deg
    #a_sph = []
    ## list to store absolute values if sperical harminics
    #phi = 0.0
    ## Fix azimuth, phi at zero
    #theta = -pi/2
    ## start theta from -90 deg
    #while theta < pi/2:
        #h = special.sph_harm(0,10, phi, theta) # (m, l , phi, theta)
        #a_sph.append(abs(h))
        #a_th.append(theta * 180/pi)
        #theta = theta + 0.02

    #plot(a_th,a_sph)
    #show()


    '''

    xyzout=array([ 12.5, -56.6 ,  250.0]) #in mm; outside array
    qxqyqz=array([.8,.078,1.578])
    from meg import makesine
    ms = makesine.create(1000, 1/p.hdr.header_data.sample_period, 30)
    lfout = leadfield.calc(p, p.data.channels, xyzout)
    s=simsource.calc(lfout, xyzout, qxqyqz)
    s=s[0,:,:]
    simd_30hz = dot(ms,s)

    simd_mix = simd_5hz + simd_30hz
    Alm_in = dot(simd_mix, Sin.T)
    Ain = dot(Alm_in, Sin)

    Alm_in = dot(simd_mix, pinv(Sin))
    Ain = dot(Alm_in, Sin)

    Alm_out = dot(simd_mix, Sout.T)
    Aout = dot(Alm_out, Sout)

    Alm_out = dot(simd_mix, pinv(Sout))
    Aout = dot(Alm_out, Sout)


    Sall = zeros((size(Sin,0)+size(Sout,0), size(Sin,1)))
    Sall[0:90] = Sin
    Sall[90:] = Sout
    Alm_all = dot(simd_mix, pinv(Sall))
    A = dot(Alm_all, Sall)
    '''
