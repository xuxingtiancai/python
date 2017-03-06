class MyDecorator(object):
    def __init__(self, arg):
        self.arg = arg

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            print "In my decorator before call, with arg %s" % self.arg
            fn(*args, **kwargs)
            print "In my decorator after call, with arg %s" % self.arg
        return decorated

@MyDecorator('arg')
def f():
    print "f"
