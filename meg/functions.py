
#from pdf2py import data

class tst():
    def __init__(self):
        pass

    def offsetcorrect2(self, start=0, end=-1):
        from meg import offset
        self.data_block = offset.correct(self.data_block, start, end)
