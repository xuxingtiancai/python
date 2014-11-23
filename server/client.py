__author__ = 'xuxing'

import threading
import socket
import time

localhost = '127.0.0.1'
port = 1234

class Handler(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((localhost, port))
        content = str(self.num)
        while True:
            client.send(content)
            content = client.recv(1024).strip()
            print self.num, content
            time.sleep(5)
        client.close()

if __name__ == '__main__':
    clients = [Handler(i) for i in range(5)]
    for c in clients:
        c.start()
