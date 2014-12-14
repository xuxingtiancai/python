#coding=gbk
__author__ = 'xuxing'
import socket
import sys

def run_client(f, t):
    server = ('127.0.0.1', 9999)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        content = raw_input('%s: ' % f)
        s.sendto('\t'.join(str(i) for i in [f, t, content]), server)
        print str(t) + ': ' + s.recv(1024)

if __name__ == '__main__':
    run_client('xuxing', 'daniu')
