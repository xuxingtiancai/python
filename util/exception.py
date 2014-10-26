

class MyException(Exception):  
    def __init__(self, msg):  
        Exception.__init__(self, msg)

try:
    raise MyException('sfsdfsd')
except MyException, e:
    print e
    print 'catch MyException'
