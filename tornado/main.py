import logging

from tornado.httpclient import AsyncHTTPClient
import tornado.httpserver   
import tornado.ioloop   
import tornado.options   
import tornado.web  
import tornado.gen
from tornado import iostream
from tornado.options import define, options   
define('port', default=8000, help='run on the given port', type=int)

from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
import socket
import functools
import struct
import json
import time
import logging

#打印时间信息
def timer(fn):
    def wrapper(*args):
        start = time.time()
        fn(*args)
        end = time.time()
        print '本次服务耗时', (end - start) * 1000, 'ms'
    return wrapper
   
#配置
predictor_conf = ()
proxy_predictor_conf = ()

#同步调用
class Sync_Handler(tornado.web.RequestHandler):   
    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
    
    def connect(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        client.connect(predictor_conf)
        return client
    
    def communicate(self, client):
        client.send(req_str)
        head = client.recv(4)
        size,= struct.unpack('!i', head)
        body = client.recv(size)
    
    def get(self):
        client = self.connect()
        for i in range(10):
            self.communicate(client)
        client.close()

def memo_async(fn):
    def wrapper(*args):
        key = args[1:]
        print wrapper.cache
        if key in wrapper.cache:
            return wrapper.cache[key]
        else:
            result = fn(*args)
            wrapper.cache[key] = result
            return result
    wrapper.cache = dict()
    return wrapper

def memo(fn):
    def wrapper(*args):
        key = args
        print wrapper.cache
        if key in wrapper.cache:
            return wrapper.cache[key]
        else:
            result = fn(*args)
            wrapper.cache[key] = result
            return result
    wrapper.cache = dict()
    return wrapper

#异步调用
class Async_Handler(tornado.web.RequestHandler):   
    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
    
    @tornado.gen.coroutine
    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        stream = IOStream(sock, IOLoop.instance())
        res = yield stream.connect(proxy_predictor_conf)
        raise tornado.gen.Return(stream)
    
    @memo_async
    @tornado.gen.coroutine
    def communicate(self, arg):
        stream = yield self.connect()
        msg = make_request(sku_id)
        yield stream.write(proxy_packed_req_str)
        head = yield stream.read_bytes(4)
        size,= struct.unpack('!i', head)
        body = yield stream.read_bytes(size)
        reply = body
        stream.close()

        raise tornado.gen.Return(reply)

    @tornado.gen.coroutine
    def get(self):
        result = yield self.communicate(arg)
        logging.info(result.query_result)

def tornado_main():
    tornado.options.parse_command_line()
    app = tornado.web.Application([
             (r"^/sync$",Sync_Handler),
             (r"^/async$",Async_Handler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)   
    http_server.listen(options.port)
    IOLoop.instance().start()

if __name__ == '__main__': 
    tornado_main()
