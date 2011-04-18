#!/usr/bin/python2
import inspect

class run:
    def __init__(self,data):
        self.out = {}
        for i in inspect.getmembers(data):
            #print eval('p.'+str(i[0]))
            self.out[i[0]] = i[1]
            #print i
            #self.out[i] = inspect.getmembers(eval('p.'+str(i[0])))

