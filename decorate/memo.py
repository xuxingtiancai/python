from functools import wraps
def memo(fn):
    @wraps(fn)
    def wrapper(*args):
        result = wrapper.cache.get(args)
        if result is None:
            result = fn(*args)
            wrapper.cache[args] = result
        return result
    wrapper.cache = {}
    return wrapper
    
def list_memo(fn):
    @wraps(fn)
    def wrapper(list_arg):
        cache_result = []
        miss_arg = []
        for arg in list_arg:
            if arg in wrapper.cache:
                cache_result.append(wrapper.cache[arg])
            else:
                miss_arg.append(arg)
        if not list_arg:
            return cache_result
        
        fn_result = fn(miss_arg)
        wrapper.cache.update(dict(zip(miss_arg, fn_result)))
        return cache_result + fn_result
