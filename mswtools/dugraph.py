'''plot du for project'''

from pylab import axes,pie,title,figure,show

### make a square figure and axes
##figure(1, figsize=(6,6))
##ax = axes([0.1, 0.1, 0.8, 0.8])
##
##labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
##fracs = [15,30,45, 10]
##
##explode=(0, 0.05, 0, 0)
##pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
##title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})
##
##show()
##
##
##        statdict = {}
##        statdict['project'] = 'test'
##        stage = os.environ['STAGE']
##        p = subprocess.Popen('du -s '+stage, shell=True, stdout=subprocess.PIPE)
##        out = p.stdout.readlines()
##        
##        statdict['Disk Usage'] = str(int(out[0].split('\t')[0])/1000.0)+'MB'
##        statdict['Disk Allocated'] = '10GB'
##        statdict['Free Space'] = str(1-(int(out[0].split('\t')[0])/1000.0)/10000)+'%'