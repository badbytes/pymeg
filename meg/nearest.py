from numpy import size, append, ndarray
def nearest(array, target):
    '''ind = fftmeg.nearest(freqlist, 40)'''
    ind = []

    for i in range(0,size(target)):

        if type(target) != list and type(target) != ndarray:
            target = [target]

        targetint = float(target[i])
        x=list(abs(array-targetint))
        ind.append(x.index(abs(array-targetint).min()))
    #ind = ind.tolist()

    return ind
