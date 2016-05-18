#######################
#性能测试工具
#######################
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
