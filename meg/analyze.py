
#from pdf2py import data

#class tst():
    #def __init__(self, data):
        #pass

    #def offsetcorrect2(self, start=0, end=-1):
        #from meg import offset
        #self.data_block = offset.correct(self.data_block, start, end)

from meg import megcontour
from meg import offset as oc

def offsetcorrect(self, start=0, end=-1):
    from meg import offset
    self.data_block = offset.correct(self.data_block, start, end)




