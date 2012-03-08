

#from meg import megcontour
#from meg import offset as oc


#class initialize:
    #def __init__(self):
        #pass
def offsetcorrect(start=0, end=-1, teset=None):
    from meg import offset
    data.data_block = offset.correct(data.data_block, start, end)




