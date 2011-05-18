from multiprocessing import Process
import threading, logging, time

def test(typetest):
    logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)
    ts = time.time(); print ts

    for i in range(3):
        if typetest == 'parrallel':
            p = Process(target=parrallel, args=(i,))
            p.start();p.join()
        elif typetest == 'threaded':
            t = threaded(args=(1))
            t.start()
        else:#if typetest != 'parrallel' and typetest != 'threaded':
            print 'test not available'
            return
        te = time.time()
    print 'elapsed time', te-ts, 'seconds'
    return
def parrallel(inputdata):

    for i in range(10000000):
        i = float(i*i)
    logging.debug('running with %s and %s');print time.time()


class threaded(threading.Thread):
    def __init__(self,group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, target=target)
        self.args = args
        self.kwargs = kwargs
        return
    def run(self):

        for i in range(10000000):
            i = float(i*i)
        logging.debug('running with %s and %s');print time.time()

from multiprocessing import Pool, Queue
from numpy import dot
def f(x):
    print 'process',x,'running'
    for i in range(500000):
        pass;#i = dot(i,i)
    print 'Done', x
    #return x*x
    #q.put(i)

if __name__ == '__main__':
    ts = time.time();
    logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

    #-----Pool
    pool = Pool(processes=2)              # start 4 worker processes
    #result = pool.apply_async(f)     # evaluate "f(10)" asynchronously
    #print result.get(timeout=1)           # prints "100" unless your computer is *very* slow
    pool.map(f, [1,2])          # prints "[0, 1, 4,..., 81]"
    logging.debug('running with %s and %s')
    te = time.time()
    print 'elapsed time', te-ts, 'seconds'

    ##----Non-Pooled
    #q = Queue()
    #q.put(1)
    #q.put(2)
    #p = Process(target=f, args=(q,))
    #p.start()
