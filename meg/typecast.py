
#thanks to christoph terasa for most of this code
#http://pastebin.com/Xsu3brSr


import numpy
import struct

def translatetype(outtype, intype):
    if outtype == 'uint8':
        o = 'I'
    if intype == 'float32' or intype == 'float':
        i = 'f'
    if intype == 'float64':
        i = 'd'
    return o,i


def typecast(x,dtype):
    """
    typecasts x to dtype MATLAB-style, i.e. returns a tuple if the new datatype is smaller than the original one

    x: number to be typecast
    dtype: new datatype x shall be cast to, either as string or numpy.dtype
    """

    dtype = numpy.dtype(dtype)
    out = dtype.type(x)
    bytes_old = x.itemsize
    bytes_new = out.itemsize
    out = []
    if bytes_new < bytes_old:
        x_dtype = x.dtype
        #print 'dt',x_dtype
        if x_dtype == 'float32' or x_dtype == 'float' or x_dtype == 'float64':
            if x_dtype == 'float32':
                outtype,intype = translatetype(dtype, x_dtype)
                x=struct.unpack(outtype,struct.pack(intype, x))#[0]
        if x_dtype == 'float64':
            x=struct.unpack('II',struct.pack('d', x))
        for j in x:
            out.append([(j>>(i*8))%(2**8) for i in range(0,bytes_old)])




    return out

