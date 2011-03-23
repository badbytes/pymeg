'''plot du for project'''

import os
import pwd
import subprocess
from matplotlib import use
use('WXAgg')
from pylab import axes,pie,title,figure,show

def diskused():
    statdict = {}
    statdict['project'] = os.environ['USER']
    stage = os.environ['STAGE']
    p = subprocess.Popen('du -s '+stage+'/data/'+os.uname()[1]+'_data0', shell=True, stdout=subprocess.PIPE)
    out = p.stdout.readlines()
    allocated = 10000000.0
    statdict['MB Used'] = (int(out[0].split('\t')[0])/1000.0)
    statdict['MB Allocated'] = allocated
    statdict['% Free'] = 100*(1-(int(out[0].split('\t')[0])/allocated))
    #statdict['Free Space'] = str(1-(int(out[0].split('\t')[0])/1000.0)/10000)+'%'
    statdict['kb-used'] = out[0].split('\t')[0]
    statdict['kb-free'] = allocated - int(out[0].split('\t')[0])
    return statdict
    
def plotdu():
    stats = diskused()
    
    figure(1, figsize=(7,7))
    ax = axes([0.1, 0.1, 0.8, 0.8])
    
    stage = os.environ['STAGE']
    id = subprocess.Popen('du -s '+stage+'/data/'+os.uname()[1]+'_data0/*', shell=True, stdout=subprocess.PIPE)
    duout = id.stdout.readlines()
    
    
    p = subprocess.Popen('ls '+stage+'/data/'+os.uname()[1]+'_data0/', shell=True, stdout=subprocess.PIPE)
    out = p.stdout.readlines()
    labels = ['free']
    dubyid = [stats['kb-free']]
    for i in range(0, len(out)):
        labels.append(out[i].split('\n')[0])
        dubyid.append(int(duout[i].split('\t')[0]))
    
    labels.append(os.uname()[1]+'_odexport/')
    od = subprocess.Popen('du -s '+stage+'/data/'+os.uname()[1]+'_odexport/', shell=True, stdout=subprocess.PIPE)
    odout = od.stdout.readlines()
    dubyid.append(int(odout[0].split('\t')[0]))

    fracs = dubyid

    #explode=(0, 0.05, 0, 0)
    pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
    title(stats['project']+' Allocation', bbox={'facecolor':'0.8', 'pad':5})
    show()

if __name__=='__main__':
    plotdu()
    
