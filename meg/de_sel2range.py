'''get_de_sel 2 range file'''

import os
import subprocess


def run(fileoutname):
    s = subprocess.Popen('get_de_selections', shell=True, stdout=subprocess.PIPE)
    out = s.stdout.readlines()
    x=out[0].split('-t')
    print x
    
    emarray = []
    for i in range(1, len(x)):
	emarray.append(eval(x[i]))
	
    STAGE = os.environ['STAGE']
    
    f = open(STAGE+'/users/ACGS/'+fileoutname+'.range','w')
    print f
    #rangelist = zeros([len(emarray),6])
    for j in range(0, len(emarray)):
	#rangelist[j,0] = emarray[j][2] #start
	#rangelist[j,1] = emarray[j][4] #end
	#rangelist[j,2] = 0 #
	#rangelist[j,3] = 0 #
	#rangelist[j,4] = 0 #
	#rangelist[j,5] = j #selection number
	
	f.write(str(emarray[j][2]*1000)+'\t')
	f.write(str(emarray[j][4]*1000)+'\t')
	f.write(str(0)+'\t')
	f.write(str(0)+'\t')
	f.write(str(0)+'\t')
	f.write(str(j)+'\n')
	
    #
    #for r in rangelist:
	#f.write()
	
if __name__ == '__main__':
    run()
