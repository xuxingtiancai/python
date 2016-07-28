__author__ = 'xuxing'
from functools import wraps

#1.1 函数-> 函数
def Decro(fn):
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

#1.2 函数 -> 函数 (带参数)
def ArgDecroForFunc(aggr, initial):
    def collect_main(fn):
        def wrapper(*args):
            return reduce(aggr, fn(*args), initial)
        return wrapper
    return collect_main
        
#2 函数 -> 类 (带参数)
def test(printValue=True):
    def _test(cls):
        def __test(*args,**kw):
            clsName=re.findall('(\w+)',repr(cls))[-1]
            print 'Call %s.__init().'%clsName
            obj=cls(*args,**kw)
            if printValue:
                print 'value = %r'%obj.value
            return obj
        return __test
    return _test

@test()
class sy(object):
    def __init__(self,value):
        self.value=value

#3 类 -> 函数 (带参数)
class ClsDecroForFunc:
    def __init__(self, arg):
        self._arg = arg

    def __call__(self, func):
        self._func = func
        return self._call
    
    def _call(self, *args, **kwargs):
        print 'ClsDecroForFunc', self._arg
        self._func(*args)
        
#4 类 -> 类 (带参数)
class test(object):
    def __init__(self,printValue=False):
        self._printValue=printValue
    
    def __call__(self, cls):
        self._cls = cls
        return self._call
        
    def _call(self, *args,**kw):
        obj = self._cls(*args,**kw)
        if self._printValue:
            print 'value = %r' % obj.value
        return obj
    
@test(True)
class sy(object):
    def __init__(self,value):
        #The parameters of _call can be '(value)' in this case.
        self.value=value


if __name__ == '__main__':
    func()

#参考链接
http://www.jb51.net/article/63892.htm
