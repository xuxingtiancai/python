__author__ = 'xuxing'

import threading
import socket

localhost = '127.0.0.1'
port = 1234

counter = 0

class Handler(threading.Thread):
    def __init__(self, server, client):
        threading.Thread.__init__(self)
        self.server = server
        self.client = client

    def run(self):
        global counter
        counter += 1
        while True:
            data = self.client.recv(1024).strip()
            self.client.send(data + data[0])
        self.client.close()

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((localhost, port))
    server.listen(1)

    while True:
        client, addr = server.accept()
        handler = Handler(server, client)
        handler.start()
