from multiprocessing import Process, Queue, JoinableQueue
import os, time, random

def write(q):
    num = 0
    while(True):
        q.put(num)
        num += 1
        time.sleep(0.2)

def read(q):
    while True:
        value = q.get()
        print 'Get %s from queue.' % value
        q.task_done()
        time.sleep(0.3)

if __name__=='__main__':
    q = JoinableQueue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.daemon = True
    pr.daemon = True
    pw.start(); time.sleep(1)
    pr.start()
    q.join()
