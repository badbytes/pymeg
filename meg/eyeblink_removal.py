

from numpy import *

def runica(data, numofcomps):
    import mdp
    ica = mdp.nodes.FastICANode(white_comp=numofcomps,verbose=True);
    comp = ica.execute(data)
    return comp, ica

def ica_correl(comp, data, channelindex):
    '''ind = p.data.channels.labellist.index('A195')
    ind = p.data.channels.labellist.index('A195')
    correlateICA(comp, data, ind)'''

    correl_list = zeros((size(comp,1),len(channelindex)))

    for j in range(0, len(channelindex)):
        print 'computing correlation coef with channel:', channelindex[j]
        for i in range(0 ,size(comp,1)):
            #correl_list.append(corrcoef(comp[:,i],data[:,j])[1,0])
            correl_list[i,j] = corrcoef(comp[:,i],data[:,channelindex[j]])[1,0]
            #print correl_list[:,j]

    print 'Me thinks comps', arange(size(comp,1))[sum(abs(correl_list),1) > .5], 'are blinks'
    blinkcomps = arange(size(comp,1))[sum(abs(correl_list),1) > .5]
    return abs(correl_list), blinkcomps
    #return array(abs(correl_list))

    #c1 = eyeblink_removal.ica_correl(comp, p.data.data_block, 193)
    #c2 = eyeblink_removal.ica_correl(comp, p.data.data_block, 210)
    #eyeblink_comps = (abs(c1) + abs(c2)) > .4

    #comp[:,eyeblink_comps] = 0

    #ip = dot(comp,ica.get_recmatrix())


