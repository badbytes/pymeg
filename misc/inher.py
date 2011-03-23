''' '''
class setupstuff:
    def __init__(self, argin):
        self.argm = argin

    #class doit:
    def doit(self, argin):
        self.e = argin+self.argm
        print self.e
        
    def getit(self):
        print self.argm
        j = setupstuff('test') #.doit('2')
        j.doit(self.argm)
        #print self.d
    
