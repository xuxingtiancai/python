#coding=gbk
__author__ = 'xuxing'
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定端口:
s.bind(('127.0.0.1', 9999))
print 'Bind UDP on 9999...'

addr_dict = dict()
while True:
    # 接收数据:
    data, addr = s.recvfrom(1024)
    f, t, content = data.split('\t', 2)
    addr_dict[f] = addr
    if t in addr_dict:
        s.sendto(content, addr_dict[t])
