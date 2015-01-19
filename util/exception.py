#错误记录
try:  
    print test1.division(10, 0)  
except:  
    print 'invoking division failed.'  
    traceback.print_exc()  
    sys.exit(1)  
    
logging.exception(ex)
logging.error(ex, exc_info=1) # 指名输出栈踪迹, logging.exception的内部也是包了一层此做法
logging.critical(ex, exc_info=1) # 更加严重的错误级别


#Exception类别
class MyException(Exception):  
    def __init__(self, msg):  
        Exception.__init__(self, msg)

try:
    raise MyException('sfsdfsd')
except MyException, e:
    print e
    print 'catch MyException'
