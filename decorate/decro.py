__author__ = 'xuxing'
from functools import wraps

def hello_world_decro(fn):
    def wrapper(*args):
        print 'hello_world_decro'
        fn(*args)
    return wrapper

#函数对象的局部变量
def immutable_member_decro(fn):
    def wrapper(*args):
        wrapper.counter += 1
        print 'counter=', wrapper.counter
        fn(*args)
    wrapper.counter = 0
    return wrapper

#闭包中存放变量
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
    
#类装饰器
def Tracer(aClass):
    class Wrapper:
        def __init__(self,*args,**kargs):
            self.fetches = 0
            self.wrapped = aClass(*args,**kargs)
        def __getattr__(self,attrname):
            print('Trace:'+attrname)
            self.fetches += 1
            return getattr(self.wrapped,attrname)
    return Wrapper

#带参数的装饰器
def collect(aggr, initial):
    def collect_main(fn):
        def wrapper(*args):
            return reduce(aggr, fn(*args), initial)
        return wrapper
    return collect_main
    
#类作为装饰器


if __name__ == '__main__':
    func()
