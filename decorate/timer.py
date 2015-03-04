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
        g = fn(*args)
        while True:
            try:
                start = time.time()
                result = g.next()
                end = time.time()
                wrapper.cost += end - start
                yield result
            except StopIteration, e:
                raise StopIteration
    wrapper.cost = 0
    return wrapper
