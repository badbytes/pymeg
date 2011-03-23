class One:
    k = 7
    def __init__(self, x):
        self.x=x


class Two(One):
    def test(self):
        print self.k
        print self.x
        

    
'''t=tap.Two(9)
t.test()'''
