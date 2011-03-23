#plot brainstuff

from pylab import *

def readcsv(filename, sep):
    #f = open(filename)
    d = {}
    x = []
    for line in open(filename,'r').readlines():
        x.append(line)


    #dataarray = zeros((len(x[0].split(',')),len(x)))
    print len(x[0].split(sep))

    for i in range(0, len(x[0].split(sep))):

        for j in range(0, len(x)):
            if j == 0:
                pass
            else:
                try:
                    val = float(x[j].split(sep)[i])
                except ValueError:
                    val = x[j].split(sep)[i]

                try:
                    val = val.replace('"','')
                except AttributeError:
                    pass

                try:
                    d[x[0].split(sep)[i].replace('"','')] = append(d[x[0].split(sep)[i].replace('"','')],val)
                except KeyError:
                    d[x[0].split(sep)[i].replace('"','')] = val



    return d

