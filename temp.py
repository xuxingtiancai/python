class dec:
    def __init__(self, f):
        self.f = f
    def __call__(self, *args):
        print "Decorating", self.f.__name__
        self.f(*args)

@dec
def f(a, b):
print "f", a, b
