def decro(cls):
    def func(self):
        print 'hello world'
    cls.func = func
    return cls

@decro
class A:
    pass
