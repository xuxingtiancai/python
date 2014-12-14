from multiprocessing import Process
import os

def run_proc(name, L):
    print 'Run child process %s (%s)...' % (name, os.getpid())
    L.append(4)
    print L

if __name__=='__main__':
    L = [1, 2, 3]
    p = Process(target=run_proc, args=('test', L))
    p.start()
    p.join()
    print L
