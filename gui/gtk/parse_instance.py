import inspect
from numpy import ndarray

class run:
    def __init__(self,data,verbose=None):
        self.out = {}
        
        if data.__class__ == dict:
            for i in data.keys():
                self.out[i] = data[i]
        if data.__class__ == ndarray:
            self.out['ndarray'] = data
        else:
            for i in inspect.getmembers(data):
                self.out[i[0]] = i[1]
        
        if verbose == False:
            for i in self.out.keys():
                if i.endswith('__'):
                    self.out.pop(i)


