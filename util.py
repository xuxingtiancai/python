#coding=utf-8

from collections import defaultdict
from functools import wraps
import traceback
import logging
import os, re, sys, time
import re
import math
from itertools import *
import json
from collections import OrderedDict

#logger
def get_logger(name, path, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s')

    if path:
        fh = logging.FileHandler(path, 'a')
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

logger = get_logger('util_logger', None, level=logging.WARN)

#装饰器
#缓存器
def memo(fn):
    @wraps(fn)
    def wrapper(*args):
        if args not in wrapper.cache:
            wrapper.cache[args] = fn(*args)
        return wrapper.cache[args]
    wrapper.cache = dict()
    return wrapper

def memo_key(key_func):
    def main(fn):
        @wraps(fn)
        def wrapper(*args):
            key = key_func(args)
            if key not in wrapper.cache:
                wrapper.cache[key] = fn(*args)
            return wrapper.cache[key]
        wrapper.cache = dict()
        return wrapper
    return main

#单例模式
def singleton(cls):
    instances = {}
    def _wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _wrapper

#收集器
def collector(c_func):
    def main(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return c_func(fn(*args, **kwargs))
        return wrapper
    return main
#计数器
def counter(key_func):
    def main(fn):
        @wraps(fn)
        def wrapper(*args):
            key = key_func(args)
            #wrapper.counter[key] += 1
            wrapper.counter[key] = wrapper.counter.get(key, 0) + 1
            return fn(*args)
        #wrapper.counter = defaultdict(lambda : 0)
        wrapper.counter = OrderedDict()
        return wrapper
    return main

#计时器
def timer(fn):
    def wrapper(*args):
        start = time.time()
        result = fn(*args)
        end = time.time()
        wrapper.cost += end - start
        return result
    wrapper.cost = 0
    return wrapper


def timer_yield(fn):
    def wrapper(*args):
        start = time.time()
        for i in fn(*args):
            end = time.time()
            wrapper.cost += end - start
            yield i
            start = time.time()
        end = time.time()
        wrapper.cost += end - start
    wrapper.cost = 0
    return wrapper

#------------------多线程------------------------------
def argMerge(fn):
    @wraps(fn)
    def wrapper(args):
        return fn(*args)
    return wrapper

@collector(list)
@argMerge
def worker(pid, fn, args, concurrency):
    num = int(math.ceil(len(args) / float(concurrency)))
    for i in xrange(num*pid, min(num*(pid+1), len(args))):
        logger.warn('pid=%d num=%d/id=%d arg=%s' % (pid, num, i-num*pid+1, args[i]))
        for res in fn(*args[i]):
            yield res

def scheduler(fn, args, concurrency):
    import multiprocessing
    pool = multiprocessing.Pool(concurrency)
    return pool.map(worker, [(i, fn, args, concurrency) for i in range(concurrency)])

#------------------多线程(文件模式)------------------------------
#合并所有文件
def merge_file(concurrency, outputPathSplit, outputPath):
    fout = open(outputPath, 'w')
    for i in range(concurrency):
        path = outputPathSplit % i
        with open(path) as fin:
            for line in fin:
                print >>fout, line[:-1]
        os.remove(path)
    fout.flush()
    fout.close()

@argMerge
def worker_file(pid, fn, args, concurrency, outputPathSplit):
    with open(outputPathSplit % pid, 'w') as fout:
        num = int(math.ceil(len(args) / float(concurrency)))
        for i in xrange(num*pid, min(num*(pid+1), len(args))):
            logger.warn('pid=%d num=%d/id=%d arg=%s' % (pid, num, i-num*pid+1, args[i]))
            if (i-num*pid+1) % 100 == 0:
                logger.error('pid=%d num=%d/id=%d arg=%s' % (pid, num, i-num*pid+1, args[i]))
            fn(fout, *args[i])

def scheduler_file(fn, args, concurrency, outputPathSplit, outputPath):
    import multiprocessing
    pool = multiprocessing.Pool(concurrency)
    pool.map(worker_file, [(i, fn, args, concurrency, outputPathSplit) for i in range(concurrency)])
    merge_file(concurrency, outputPathSplit, outputPath)

#--------------读取网页 & 重试机制-----------------------------------------------
def retrier(retryMax, returnFn=lambda *args, **kwrags:None):
    def main(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for i in range(retryMax):
                try:
                    logger.warn('function=%s args=%s retry=%d/%d' % (fn.__name__, args, i+1, retryMax))
                    return fn(*args, **kwargs)
                except Exception, e:
                    #logger.error(traceback.format_exc())
                    if i == retryMax - 1:
                        logger.error('{0}{1} e={2}'.format(fn.__name__, args, e))
                    pass
            return returnFn(*args, **kwargs)
        return wrapper
    return main

def proxy_scheduler():
    def main(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            wrapper.count += 1
            #重新载入
            if not wrapper.proxy_list or wrapper.count % 10000 == 1:
                try:
                    proxy_list = []
                    response = urllib2.urlopen('http://ent.kuaidaili.com/api/getproxy?orderid=906286745929487&num=500&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&sp2=1&quality=1')
                    for line in response:
                        line = line.strip()
                        if line:
                            proxy_list.append(line)
                    wrapper.proxy_list = proxy_list
                except:
                    pass
            if not wrapper.proxy_list:
                raise Exception('no proxy')

            ip, port = wrapper.proxy_list[wrapper.index].split(':')
            protocal = '{0}:{1}'.format(ip, port)
            wrapper.index = (wrapper.index + 1) % len(wrapper.proxy_list)
            wrapper.protocal = protocal
            wrapper.count_dic[protocal] += 1
            logger.warn(protocal)

            proxy = urllib2.ProxyHandler({'http': protocal, 'https': protocal})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            return fn(*args, **kwargs)
        wrapper.count = 0
        wrapper.proxy_list = None
        wrapper.index = 0
        wrapper.protocal = None
        wrapper.error_dic = defaultdict(lambda : 0)
        wrapper.count_dic = defaultdict(lambda : 0)
        return wrapper
    return main

import urllib2
from bs4 import BeautifulSoup

def readPage(url, timeout_, **kwargs):
    data = kwargs.get('data', None)
    headers = kwargs.get('headers', dict())
    path = kwargs.get('download', None)
    sleep = kwargs.get('sleep', 0)

    if path and os.path.exists(path):
        html = open(path).read()
    else:
        time.sleep(sleep)
        request = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(request, timeout=timeout_)
        html = response.read()
        if path:
            with open(path, 'w') as fout:
                fout.write(html)
    return html

def readPage_Soup(url, timeout_, encoding, **kwargs):
    parser = kwargs.get('parser', 'html.parser')
    html = readPage(url, timeout_, **kwargs)
    return BeautifulSoup(html, parser, from_encoding=encoding)

def readPage_Json(url, timeout_, encoding, **kwargs):
    html = readPage(url, timeout_, **kwargs)
    return json.loads(html, encoding=encoding)

def url2path(url):
    path = url
    path = re.sub(r'[/\?:]', r'_', path)
    path = re.sub(r'_+', r'_', path)
    return path

#------------解析json文件------------------------------------------------
#辅助函数
def trans_text(s, encoding='gb18030'):
    if not isinstance(s, (str, unicode)):
        s = str(s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = s.encode(encoding)
    return s

def parse_jsonFile(inpath, outpath, **kwargs):
    limit = kwargs.get('limit', None)
    with open(outpath, 'w') as fout:
        for line in islice(open(inpath), 0, limit):
            try:
                obj = json.loads(line, object_pairs_hook=OrderedDict)
                parse_jsonObj(0, obj, fout)
                print >>fout, ''
            except:
                continue

def parse_jsonObj(offset, obj, fout):
    if isinstance(obj, dict):
        for k, v in obj.iteritems():
            if not isinstance(v, (dict, list)):
                print >>fout, '\t'*offset + trans_text(k) + '\t' + trans_text(v)
            else:
                print >>fout, '\t'*offset + k
                parse_jsonObj(offset+1, v, fout)
    elif isinstance(obj, list):
        for i in obj:
            parse_jsonObj(offset, i, fout)
    else:
        text = trans_text(obj)
        if text:
            print >>fout, '\t'*offset + text
