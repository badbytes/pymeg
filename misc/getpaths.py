'''regexp mass file read
paths,files = getpaths.getpathtofiles('/opt/msw_danc/data/spartan_data0','_file$')
paths,files = getpaths.getpathtofiles('/opt/msw_danc/data/spartan_data0','bahe.*bahe.*25$')
'''

import os,re

def getpathtofiles(dir, filestringtolookfor):
    paths = []
    filesfound = []

    for path, dirs, files in os.walk(dir):
        #print path, dirs, files
        for f in files:
            x = re.search(filestringtolookfor, f)
            try:
                x.end()
                paths.append(path)
                filesfound.append(f)
            except AttributeError:
                pass

    return paths,filesfound
