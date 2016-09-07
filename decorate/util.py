#coding=gbk

from collections import defaultdict
from functools import wraps

def collector(c_func):
    def main(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return c_func(fn(*args, **kwargs))
        return wrapper
    return main

def memo(fn):
    @wraps(fn)
    def wrapper(*args):
        result = wrapper.cache.get(args)
        if result is None:
            result = fn(*args)
            wrapper.cache[args] = result
        return result
    wrapper.cache = dict()
    return wrapper

def counter(key_func):
    def main(fn):
        @wraps(fn)
        def wrapper(*args):
            key = key_func(args)
            wrapper.counter[key] += 1
            return fn(*args)
        wrapper.counter = defaultdict(lambda : 0)
        return wrapper
    return main

@collector(set)
def test_gen():
    for i in range(10):
        yield i

if __name__ == '__main__':
    print test_gen.__name__
