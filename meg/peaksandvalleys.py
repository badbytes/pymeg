
def detect(inputdata):
    ind = []; di = []; sw = [];peakind = []; valleyind = []
    x = inputdata
    for i in range(0, len(x)):
        try:
            d = z - x[i]
            if d < 0: #downslope
                sw.append(-1)
            if d > 0: #upslope
                sw.append(1)
            if d == 0: #upslope
                sw.append(sw[-1])
            try:
                if sw[-2] != sw[-1]:
                    ind.append(i-1)
                    if sw[-1] == -1:
                        valleyind.append(i-1)
                    if sw[-1] == 1:
                        peakind.append(i-1)
            except:
                pass

            di.append(d)
            z = x[i]
        except NameError: #first instance
            z = x[i]
            sw.append(0)
    ind.pop(0) #remove first point

    return peakind,valleyind
