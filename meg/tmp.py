##for i in range(11):
##    if i==0:
##        x=t.datapiece.data_blockall[t.datapiece.trigind.trigstartind[i]:t.datapiece.trigind.trigstartind[i]+700,:]
##    else:
##        x=t.datapiece.data_blockall[t.datapiece.trigind.trigstartind[i]:t.datapiece.trigind.trigstartind[i]+700,:]+x/2
##        

def test(var):
    x=var
    try: x
    except NameError:
        return False
    else:
        return True
    