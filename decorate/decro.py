__author__ = 'xuxing'
from functools import wraps

def hello_world_decro(fn):
    def wrapper(*args):
        print 'hello_world_decro'
        fn(*args)
    return wrapper

def immutable_member_decro(fn):
    def wrapper(*args):
        wrapper.counter += 1
        print 'counter=', wrapper.counter
        fn(*args)
    wrapper.counter = 0
    return wrapper

def mutable_member_decro(fn):
    counter = []
    def wrapper(*args):
        counter.append('')
        print 'counter=', counter
        fn(*args)
    return wrapper

@mutable_member_decro
def func():
    print 'func'


if __name__ == '__main__':
    func()
    func()
